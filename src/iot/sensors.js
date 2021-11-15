
let temp = 0
function updateTemperature() {
    temp += 0.1
    return temp
}

function updateHumidity() {
    return temp
}

function updatePressure() {
    return temp
}

function updateCO2() {
    return temp
}

function updateQuality() {
    return temp
}

function updateWind() {
    return temp
}

function updateUV() {
    return temp
}

function updateRain() {
    return temp
}

module.exports = {
    temp: updateTemperature,
    hum: updateHumidity,
    press: updatePressure,
    co2TVOC: updateCO2,
    qual: updateQuality,
    wind: updateWind,
    uv: updateUV,
    rain: updateRain
}