var randRange = function(n, vMin, vMax) {
	return numeric.add(numeric.mul((vMax - vMin), numeric.random([1, n])), vmin);
};	

var theta = numeric.linspace(-4 * Math.pi, 4 * Math.pi, 100);
var z = numeric.linspace(-2, 2, 100);
var r = numeric.add(numeric.pow(z, 2), 1);

var x = numeric.mul(r, numeric.sin(theta));
var y = numeric.mul(r, numeric.cos(theta));

var spiral = {
	x: x,
	y: y,
	z: z,
	mode: 'markers',
	marker: {
		size: 12,
		line: {
			color: 'rgba(217, 217, 217, 0.14)',
			width: 0.5
		},
		opacity: 0.8,
	},
	type: 'scatter3d'
};


