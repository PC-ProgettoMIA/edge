# TODO change initialization as mqtt_mia.py
# TODO change quality name (il nome delle pm dà errore il . con mongo)

from aiohttp import web
import atomic_store
import time
import board
import busio
import adafruit_bmp280
import adafruit_si7021
import adafruit_sgp30
import serial
import RPi.GPIO as GPIO
import smbus
import random
import json
import threading
import uuid

namespace = "my.sensors:"

# ***********************************************************
# *                  isr routine anemometer                 *
# ***********************************************************

_MIN_ANE_FRQ = 0.25


def isr_routine(channel):
    elapsed_time = time.perf_counter()
    f = (1 / (elapsed_time - ane_wind.get_last_time())) / 2
    if f <= ane_wind.get_max_hz():
        ane_wind.set_last_time(elapsed_time)
        ane_wind.set_frq(f)
        if ane_wind.get_frq() <= _MIN_ANE_FRQ:
            ane_wind.set_frq(0)

    #print("speed m/s %.2f  ID:%i" % (ane_wind.read(), ane_wind.uni))
    # else:
    #    print("\x1B[31m" "Anemometer frq error %.2f" "\x1B[0m" % f)


# ***********************************************************
# *                    class anemometer                     *
# ***********************************************************

_INTERRUPT_PIN = 4


class anemometer:
    def __init__(self):
        self.__x_hz = [0, 3.25, 4.64, 6.39, 8.05, 10.17, 12.23,
                       14.28, 16.92, 19.34, 21.59, 23.53, 24.70, 32.58]  # Hz
        self.__y_ms = [0, 4.06, 5.37, 6.89, 8.85, 11.33, 13.13,
                       15.49, 17.81, 20.31, 22.61, 24.39, 24, 56, 32.4]  # m/s

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(_INTERRUPT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            _INTERRUPT_PIN, GPIO.FALLING, callback=isr_routine)

        self.__frq = 0
        self.__last_time = 0
        #self.uni = random.randint(0,9999)
        #print("random ID object ", self.uni)
        #print("GPIO SET FOR INTERRUPT ON PIN %i" % _INTERRUPT_PIN)

    def read(self):
        i = 0

        if self.__frq >= self.__x_hz[-1]:
            return self.__y_ms[-1]

        while self.__frq > self.__x_hz[i]:
            i += 1

        return (self.__y_ms[i] - self.__y_ms[i-1]) * (self.__frq - self.__x_hz[i-1]) / (self.__x_hz[i] - self.__x_hz[i-1]) + self.__y_ms[i-1]

    def get_max_hz(self):
        return self.__x_hz[-1]

    def get_last_time(self):
        return self.__last_time

    def set_last_time(self, val):
        self.__last_time = val

    def get_frq(self):
        return self.__frq

    def set_frq(self, val):
        self.__frq = val

    def __del__(self):
        print("destroy object anemometer")
        GPIO.cleanup()


# ******************************************************
# *  Class ads1115 ADC read uv_sensor and rain_sensor  *
# ******************************************************
_DEVICE_ADDR = 0x48      # 7 bit address << 1
# main register of device set this for navigate in register device
_PONITER_REG_ADDR = 0x00
_CONVERSION_REG_ADDR = 0x00      # cmd for read register conversion
_CONFIG_REG_ADDR = 0x01
_SET_CHANNEL_AN1_MSB = 0b11010011
_SET_CHANNEL_AN1_LSB = 0b10000011
_SET_CHANNEL_AN3_MSB = 0b11110011
_SET_CHANNEL_AN3_LSB = 0b10000011
_TRHD_IS_RAIN = 18000
_THRD_IS_NOT_RAIN = 18500
_MIN_SENS_RAIN_VAL = 9000
_MAX_SENS_RAIN_VAL = 26210
_SENS_UV_VAL_NC = 5000
_MIN_SENS_UV_VAL = 8000
_MAX_SENS_UV_VAL = 17600
_MAX_SENS_UV_VAL_MW_CM_2 = 10
_CONVERSION_TIME = 0.010


class ads1115:
    def __init__(self, bus_i2c):
        # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self.bus = smbus.SMBus(bus_i2c)
        self. uv = 0
        self.rain = False

    def read_sensor_uv(self):
        buffer_i2c_data = bytearray(2)

        # Select pin An1 for start a AD conversion
        self.bus.write_i2c_block_data(_DEVICE_ADDR, _CONFIG_REG_ADDR, [
                                      _SET_CHANNEL_AN1_MSB, _SET_CHANNEL_AN1_LSB])
        # wait until data conversion is finish 10ms at 128SPS
        time.sleep(_CONVERSION_TIME)
        # set coversion addres for read
        self.bus.write_byte_data(
            _DEVICE_ADDR, _PONITER_REG_ADDR, _CONVERSION_REG_ADDR)
        buffer_i2c_data = self.bus.read_i2c_block_data(
            _DEVICE_ADDR, _PONITER_REG_ADDR, 2)
        an1_val = buffer_i2c_data[0] << 8 | buffer_i2c_data[1]
        # process data value an1
        if an1_val < _SENS_UV_VAL_NC:
            self.uv = -1
        elif an1_val < _MIN_SENS_UV_VAL:
            self.uv = 0
        else:
            self.uv = (an1_val - _MIN_SENS_UV_VAL) * \
                (_MAX_SENS_UV_VAL_MW_CM_2 / (_MAX_SENS_UV_VAL - _MIN_SENS_UV_VAL))

        return self.uv

    def read_sensor_rain(self):
        buffer_i2c_data = bytearray(2)

        # Select pin An3 for start a AD conversion
        self.bus.write_i2c_block_data(_DEVICE_ADDR, _CONFIG_REG_ADDR, [
                                      _SET_CHANNEL_AN3_MSB, _SET_CHANNEL_AN3_LSB])
        # wait until data conversion is finish 10ms at 128SPS
        time.sleep(_CONVERSION_TIME)
        # set coversion addres for read
        self.bus.write_byte_data(
            _DEVICE_ADDR, _PONITER_REG_ADDR, _CONVERSION_REG_ADDR)
        buffer_i2c_data = self.bus.read_i2c_block_data(
            _DEVICE_ADDR, _PONITER_REG_ADDR, 2)
        an3_val = buffer_i2c_data[0] << 8 | buffer_i2c_data[1]
        # process data value an3
        if an3_val > _MIN_SENS_RAIN_VAL:
            if an3_val < _TRHD_IS_RAIN:
                self.rain = True
            elif an3_val > _THRD_IS_NOT_RAIN:
                self.rain = False

        return self.rain

    def __del__(self):
        self.bus.close()


# **************************************************************************************
# *                         Class PMS5003 PM10 sens                                    *
# **************************************************************************************
# * self.pm_data [0]  = PM1.0 concentration unit μg/m3（CF=1，standard particle)       *
# * self.pm_data [1]  = PM2.5 concentration unit μg/m3（CF=1，standard particle)       *
# * self.pm_data [2]  = PM10  concentration unit μg/m3（CF=1，standard particle)       *
# * self.pm_data [3]  = PM1.0 concentration unit μg/m3（under atmospheric environment) *
# * self.pm_data [4]  = PM2.5 concentration unit μg/m3（under atmospheric environment) *
# * self.pm_data [5]  = PM10  concentration unit μg/m3（under atmospheric environment) *
# * self.pm_data [6]  = Number of particles with diameter beyond 0.3um in 0.1L of air  *
# * self.pm_data [7]  = Number of particles with diameter beyond 0.5um in 0.1L of air  *
# * self.pm_data [8]  = Number of particles with diameter beyond 1.0um in 0.1L of air  *
# * self.pm_data [9]  = Number of particles with diameter beyond 2.5um in 0.1L of air  *
# * self.pm_data [10] = Number of particles with diameter beyond 5.0um in 0.1L of air  *
# * self.pm_data [11] = Number of particles with diameter beyond 10um in 0.1L of air   *
# **************************************************************************************

class pms5003:
    def __init__(self, ser_port):
        self.ser = serial.Serial(
            ser_port, baudrate=9600, stopbits=1, parity="N", timeout=2)
        __PASSIVE_MODE = b'\x42\x4d\xe1\x00\x00\x01\x70'  # imposto Passive Mode
        self.ser.write(__PASSIVE_MODE)
        self.pm_data = [0] * 12

    def read(self):
        check = 0
        self.ser.flushInput()
        __READ_MODE = b'\x42\x4d\xe2\x00\x00\x01\x71'
        self.ser.write(__READ_MODE)
        buffer_data = self.ser.read(32)
        # Check if data header is correct
        # try:
        if buffer_data[0] == int("42", 16) and buffer_data[1] == int("4d", 16):
            #print("Header is correct")
            cs = buffer_data[30] << 8 | buffer_data[31]   # check sum
            # Calculate check sum value
            for i in range(30):
                check += buffer_data[i]
                # Check if check sum is correct
            if check == cs:
                for i in range(12):
                    self.pm_data[i] = buffer_data[i * 2 +
                                                  4] << 8 | buffer_data[i * 2 + 5]

                # return self.pm_data

                val_ret = {"pm1.0_std": self.pm_data[0], "pm2.5_std": self.pm_data[1], "pm10_std ": self.pm_data[2],
                           "pm1.0_atm": self.pm_data[3], "pm2.5_atm": self.pm_data[4], "pm10_atm ": self.pm_data[5],
                           "part_0.3 ": self.pm_data[6], "part_0.5 ": self.pm_data[7], "part_1.0 ": self.pm_data[8],
                           "part_2.5 ": self.pm_data[9], "part_5.0 ": self.pm_data[10], "part_10  ": self.pm_data[11]}

                return val_ret

        else:
            #print("Header corrupt PMS5003")
            return -1

        # except Exception:
        #        print("PMS5003 Errore trasmissione dati")

    def data_print(self):
        print("Standard particle        : PM1=%d    PM2.5=%d    PM10=%d ug/m^3 \033[0K" % (
            self.pm_data[0], self.pm_data[1], self.pm_data[2]))
        print("Atmospheric conditions   : PM1=%d    PM2.5=%d    PM10=%d ug/m^3 \033[0K" % (
            self.pm_data[3], self.pm_data[4], self.pm_data[5]))
        print("Number of particles um   : >0.3=%d    >0.5=%d    >1.0=%d  #cm^3 \033[0K" % (
            self.pm_data[6], self.pm_data[7], self.pm_data[8]))
        print("Number of particles um   : >2.5=%d    >5.0=%d    >10.0=%d #cm^3 \033[0K" % (
            self.pm_data[9], self.pm_data[10], self.pm_data[11]))

    def __del__(self):
        self.ser.close()


adc = ads1115(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

ane_wind = anemometer()

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

Si7021 = adafruit_si7021.SI7021(i2c)

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

pm_sensor = pms5003("/dev/ttyS0")

# **************************************************************************************
# *                         GET functions for the clients                              *
# **************************************************************************************


async def getTemp(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"temp": props["temperature"]["data"]})


async def getHum(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"hum": props["humidity"]["data"]})


async def getPress(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"press": props["pressure"]["data"]})


async def getCO2TVOCs(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"co2": props["co2"]["data"], "tvoc": props["tvoc"]["data"]})


async def getQuality(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"qual": props["quality"]["data"]})


async def getRain(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"rain": props["rain"]["data"]})


async def getUV(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"uv": props["uv"]["data"]})


async def getWind(request):
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"wind": props["wind"]["data"]})

# **************************************************************************************
# *   Functions to read the initial config from file and initialize the digital twin   *
# **************************************************************************************


def read_config():
    with open("config/config.json") as config_file:
        config_json = json.load(config_file)
        if "gps" not in config_json:
            print("Error! GPS required!")
        return config_json


def init(store):
    config_json = read_config()
    gps = config_json["gps"]
    serial_number = config_json["serial number"]
    school = config_json["school"]

    id = namespace + "sensor" + str(uuid.uuid4())
    store.value = {"thingId": id,
                   "policyId": "my.test:policy",
                   "attributes": {
                       "location": {
                               "position": {
                                   "latitude": gps["lat"],
                                   "longitude": gps["lon"]
                               }
                       },
                       "school": school,
                       "serial number": serial_number
                   },
                   "features": {
                       "measurements": {
                           "properties": {
                               "temperature": {
                                   "sensor": "Si7021",
                               },
                               "humidity": {
                                   "sensor": "Si7021",
                               },
                               "pressure": {
                                   "sensor": "BMP280",
                               },
                               "co2": {
                                   "sensor": "SGP30",
                               },
                               "tvoc": {
                                   "sensor": "SGP30",
                               },
                               "quality": {
                                   "sensor": "PMS5003",
                               },
                               "rain": {
                                   "sensor": "rain sensor",
                               },
                               "uv": {
                                   "sensor": "UV sensor",
                               },
                               "wind": {
                                   "sensor": "anemometer",
                               },


                           }
                       }
                   }
                   }
    store.commit()

# **************************************************************************************
# *            Functions to update the digital twin and send it to the cloud           *
# **************************************************************************************


def update():
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        timestamp = time.time()
        temperature = Si7021.temperature
        humidity = Si7021.relative_humidity
        pressure = bmp280.pressure
        co2 = sgp30.eCO2
        tvoc = sgp30.TVOC
        quality = pm_sensor.read()
        rain = adc.read_sensor_rain()
        uv = adc.read_sensor_uv()
        wind = ane_wind.read()
        if temperature != None:
            props["temperature"]["timestamp"] = timestamp
            props["temperature"]["data"] = temperature
        if humidity != None:
            props["humidity"]["timestamp"] = timestamp
            props["humidity"]["data"] = humidity
        if pressure != None:
            props["pressure"]["timestamp"] = timestamp
            props["pressure"]["data"] = pressure
        if co2 != None:
            props["co2"]["timestamp"] = timestamp
            props["co2"]["data"] = co2
        if tvoc != None:
            props["tvoc"]["timestamp"] = timestamp
            props["tvoc"]["data"] = tvoc
        if quality != None and quality != {}:
            props["quality"]["timestamp"] = timestamp
            props["quality"]["data"] = quality
        if rain != None:
            props["rain"]["timestamp"] = timestamp
            props["rain"]["data"] = rain
        if uv != None:
            props["uv"]["timestamp"] = timestamp
            props["uv"]["data"] = uv
        if wind != None:
            props["wind"]["timestamp"] = timestamp
            props["wind"]["data"] = wind

        dt["features"]["measurements"]["properties"] = props
        store.value = dt
        store.commit()


def loop_forever():
    while True:
        update()  # separare se si vuole aggiornare e inviare al cloud con timing differente
        time.sleep(1)


app = web.Application()
app.add_routes([web.get('/api/temp', getTemp),
                web.get('/api/hum', getHum),
                web.get('/api/press', getPress),
                web.get('/api/co2TVOC', getCO2TVOCs),
                web.get('/api/qual', getQuality),
                web.get('/api/rain', getRain),
                web.get('/api/uv', getUV),
                web.get('/api/wind', getWind)])

# TODO: read from config.json gps and generate a thing uuid
if __name__ == '__main__':
    with atomic_store.open('digital_twin.json', default=dict()) as store:
        if store.value == dict():
            init(store)
    loop = threading.Thread(target=loop_forever)
    loop.start()
    web.run_app(app)
