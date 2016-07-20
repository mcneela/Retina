var express = require("express");
var bodyParser = require('body-parser');
var fovea = require('../fovea.js');
/*
var mongo = require('mongodb'),
	Server = mongo.Server,
	Db = mongo.db;
var mongoose = require('mongoose');
*/

var app = express();
var layers = {};

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8000;

var router = express.Router();

router.get('/', function(req, res) {
	res.json({ message: "Welcome to the Fovea API" });
	var lay = new fovea.Layer2D("red", "layer");
	console.log(lay.name);
});

app.use('/api', router);

app.post("/api/layers", function(req, res) {
	var layerObj = new fovea.Layer2D(req.body.name, req.body.graphDiv);
	layers[req.body.name] = layerObj; 
	res.send('New layer successfully created');
});

app.post("/api/layers/hide", function(req, res) {
	layers[req.body.name].hide();
});

app.get("/api/layers/:name", function(req, res) {
	console.log(req.params.name);
	console.log(layers[req.params.name]);
	console.log(layers);
	res.send(layers[req.params.name]);	
});

app.post("/api/layers/addTrace", function(req, res) {
	var layer = layers[req.body.name];
	console.log(req.body);
	console.log(req.body.trace);
	console.log(layer);
	console.log(layer.addTrace);
	layer.addTrace[0](req.body.trace);
});

app.listen(port);
console.log("You are now accessing the Fovea API on port " + port);
