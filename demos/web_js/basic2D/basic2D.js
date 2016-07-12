// This demo uses the library NumericJS for
// numpy-like matrix computations.

var base_x = numeric.linspace(-2, 2, 50);
var quad_y = numeric.pow(base_x, 2);
var cube_y = numeric.pow(base_x, 3);
var quart_y = numeric.pow(base_x, 4);

var div = document.getElementById('2Dplot');

var quadratic = {
	x: base_x,
	y: quad_y,
	mode: 'lines'
};

var cubic = {
	x: base_x,
	y: cube_y,
	mode: 'lines'
};

var quartic = {
	x: base_x,
	y: quart_y,
	mode: 'lines'
};

var evenPowers = new Layer2D("evenPowers", div);
var oddPowers = new Layer2D("oddPowers", div);

oddPowers.addTrace(cubic);
evenPowers.addTrace(quadratic);
evenPowers.addTrace(quartic);

var traces = [quadratic, cubic, quartic];

Plotly.plot(div, traces);
