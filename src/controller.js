const dt_instance = require("./iot/dt_instance");
const dt = dt_instance.instance;

exports.getProperty = (name) => async (req, res) => {
    let feature = await dt.get("features")
    let property = feature[name]
    if (property) {
        let response = {}
        response[name] = property.properties.value
        return res.status(200).json(response);
    }
    return res.status(400).send("The digital twin has no property '" + name + "'")
};

