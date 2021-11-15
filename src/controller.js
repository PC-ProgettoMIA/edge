const dt_instance = require("./iot/dt_instance");
const dt = dt_instance.instance;

exports.getProperty = (name) => async (req, res) => {
    let property = await dt.get(name)
    if (property) {
        return res.status(200).json({ name: property });
    }
    return res.status(400).send("The digital twin has no property '" + name + "'")
};

