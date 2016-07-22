var express = require("express");
var bodyParser = require('body-parser');
var fovea = require('../fovea.js');
var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');
var plotly = require('plotly');
var $ = cheerio.load(fs.readFileSync('scatter-mode.html').toString());
/*
var mongo = require('mongodb'),
	Server = mongo.Server,
	Db = mongo.db;
var mongoose = require('mongoose');
*/

var div = $("#e215ba24-5ac3-4e3f-b126-80b127bbb9f6");
plotly.newPlot([], div);
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
	var div = $('#' + req.body.graphDiv);
	console.log(div.attr('src'));
	var layerObj = new fovea.Layer2D(req.body.name, div);
	console.log(div.data.toString());
	layers[req.body.name] = layerObj; 
	res.send('New layer successfully created');
});

app.post("/api/layers/hide", function(req, res) {
	console.log(layers[req.body.name]);
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
	layer.addTrace(req.body.trace);
	res.send('Trace successfully added.');
});

app.listen(port);
console.log("You are now accessing the Fovea API on port " + port);
