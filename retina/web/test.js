//@sourceURL=test.js

var pointCount = 31;
var i, r;
var graph = document.getElementById('graph');
var x = [];
var y = [];
var z = [];
var c = [];

for(i = 0; i < pointCount; i++){
	r = 10 * Math.cos(i / 10);
	x.push(r * Math.cos(i));
	y.push(r * Math.sin(i));
	z.push(i);
	c.push(i);
};

plotTrace = [{
  type: 'scatter3d',
  mode: 'lines+markers',
  x: x,
  y: y,
  z: z,
  line: {
    width: 6,
    color: c,
    colorscale: "Viridis"},
  marker: {
    size: 3.5,
    color: c,
    colorscale: "Greens",
    cmin: -20,
    cmax: 50
  }},                  
];

myLayer = new Layer("myLayer");
myLayer.addTrace(plotTrace);
for (var item in myLayer) {
	console.log(myLayer[item]);
	}

debugger
myLayer.hide();
Plotly.plot(graph, plotTrace);

