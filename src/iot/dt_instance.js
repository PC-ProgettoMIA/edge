const jsoning = require('jsoning');
const fs = require("fs");
const { v4: uuidv4 } = require('uuid');
const sensors = require('./sensors');
const dt = new jsoning("digital_twin.json");
const config_path = "config/config.json"
const namespace = "projectMIA"

initialize()

setInterval(async function () {
    await updateSensorValues()

}, 1000)


//id and gps set in the initialization
//TODO uniform to eclipse ditto model
async function initialize() {
    let id = await dt.get("id")

    //set the id the first time
    if (!id) {
        let id = namespace + ":" + uuidv4()
        await dt.set("id", id)
    }

    let gps = await dt.get("gps")

    //set the gps the first time
    if (!gps) {
        gps = setGPS()
        await dt.set("gps", gps)
    }
}

//TODO add exception for gps not present?
function setGPS() {
    let gps = {}
    if (fs.existsSync(config_path)) {
        data = fs.readFileSync(config_path);
        gps = JSON.parse(data).gps;
    }
    return gps
}


async function updateSensorValues() {
    //read from GPIO
    let temperature = sensors.temp()
    let humidity = sensors.hum()
    let pressure = sensors.press()
    let co2 = sensors.co2TVOC()
    let quality = sensors.qual()
    let wind = sensors.wind()
    let uv = sensors.uv()
    let rain = sensors.rain()
    await dt.set("temp", temperature)
    await dt.set("hum", humidity)
    await dt.set("press", pressure)
    await dt.set("co2TVOC", co2)
    await dt.set("qual", quality)
    await dt.set("wind", wind)
    await dt.set("uv", uv)
    await dt.set("rain", rain)

}

module.exports = { instance: dt }