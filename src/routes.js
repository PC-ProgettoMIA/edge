module.exports = function (app) {

    const controller = require("./controller");


    app.route("/api/temp")
        .get(controller.getProperty("temp"));

    app.route("/api/hum")
        .get(controller.getProperty("hum"));

    app.route("/api/press")
        .get(controller.getProperty("press"));

    app.route("/api/co2TVOC")
        .get(controller.getProperty("co2TVOC"));

    app.route("/api/qual")
        .get(controller.getProperty("qual"));

    app.route("/api/wind")
        .get(controller.getProperty("wind"));

    app.route("/api/uv")
        .get(controller.getProperty("uv"));

    app.route("/api/rain")
        .get(controller.getProperty("rain"));
};
