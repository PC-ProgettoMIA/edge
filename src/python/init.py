import atomic_store
import json
import uuid

namespace = "my.houses:"

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
    random = str(uuid.uuid4())
    id = namespace + "house" + random
    store.value = {"thingId": id,
                   "policyId": "house.mia:policy",
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


if __name__ == '__main__':
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        if store.value == dict():
            init(store)
