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
    let id = await dt.get("thingId")

    //set the id the first time
    if (!id) {
        let id = namespace + ":" + uuidv4()
        await dt.set("thingId", id)
    }

    let attributes = await dt.get("attributes")

    if (!attributes) {
        let gps = setGPS()
        let att = {
            gps: gps
        }
        await dt.set("attributes", att)
    }

    await dt.set("features", {
        temp: { properties: {} },
        hum: { properties: {} },
        press: { properties: {} },
        co2TVOC: { properties: {} },
        qual: { properties: {} },
        wind: { properties: {} },
        uv: { properties: {} },
        rain: { properties: {} }
    })

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

    let time = Date.now()

    let features = await dt.get("features")

    if (temperature != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: temperature
        }
        features.temp.properties = props
    }
    else {
        features.temp.properties.connected = false
    }

    if (humidity != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: humidity
        }
        features.hum.properties = props
    }
    else {
        features.hum.properties.connected = false
    }

    if (pressure != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: pressure
        }
        features.press.properties = props
    }
    else {
        features.press.properties.connected = false
    }

    if (co2 != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: co2
        }
        features.co2TVOC.properties = props
    }
    else {
        features.co2TVOC.properties.connected = false
    }

    if (quality != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: quality
        }
        features.qual.properties = props
    }
    else {
        features.qual.properties.connected = false
    }

    if (co2 != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: co2
        }
        features.co2TVOC.properties = props
    }
    else {
        features.co2TVOC.properties.connected = false
    }

    if (wind != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: wind
        }
        features.wind.properties = props
    }
    else {
        features.wind.properties.connected = false
    }

    if (uv != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: uv
        }
        features.uv.properties = props
    }
    else {
        features.uv.properties.connected = false
    }

    if (rain != null) { //if sensor broken
        let props = {
            connected: true,
            timestamp: time,
            value: rain
        }
        features.rain.properties = props
    }
    else {
        features.rain.properties.connected = false
    }

    await dt.set("features", features)



}

module.exports = { instance: dt }