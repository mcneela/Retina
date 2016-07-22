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

plotTrace = {
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
  }};

myLayer = new Layer3D("myLayer", graph);
myLayer.addTrace(plotTrace);
myLayer.safeHide();

var hideBtn = document.createElement("BUTTON");
var hbtnText = document.createTextNode("Hide Layer");
var showBtn = document.createElement("BUTTON");
var sbtnText = document.createTextNode("Show Layer");

hideBtn.appendChild(hbtnText);
hideBtn.onclick = function() {
	myLayer.hide();
};
document.body.appendChild(hideBtn);

showBtn.appendChild(sbtnText);
showBtn.onclick = function() {
	myLayer.show();
};

Icons = {
	'layer': {
        'width': 512,
        'path': 'M45.297,21.946l9.656-5.517L27.477,0.825L0,16.429l9.656,5.517L0,27.429l9.656,5.517L0,38.429l27.477,15.698l27.476-15.698  l-9.656-5.483l9.656-5.517L45.297,21.946z M27.477,3.125l23.435,13.309l-23.435,13.39L4.041,16.434L27.477,3.125z M11.675,23.099  l15.802,9.028l15.802-9.028l7.633,4.335l-23.435,13.39L4.041,27.434L11.675,23.099z M50.912,38.434l-23.435,13.39L4.041,38.434  l7.634-4.335l15.802,9.028l15.802-9.028L50.912,38.434z',
	 	'ascent': 850,
        'descent': -150,
    }
};

layerButton = {
	name: 'Toggle Display',
	title: 'Toggle the display of the currently selected items',
	icon: Icons.layer,
	click: function() {
		myLayer.toggleDisplay();
	}
};
document.body.appendChild(showBtn);

Plotly.newPlot(graph, [plotTrace], {title: "Is this button here?"}, {modeBarButtonsToAdd: [layerButton]});
