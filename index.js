const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const http = require("http").Server(app);


global.appRoot = path.resolve(__dirname);

const PORT = 3001;

app.use(cors());

//Per gestire i parametri passati nel corpo della richiesta http.
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const routes = require("./src/routes");
routes(app);

app.use(function (req, res) {
    res.status(404).send({ url: req.originalUrl + " not found" });
});

http.listen(PORT, function () {
    console.log("Node API server started on port " + PORT);
});

