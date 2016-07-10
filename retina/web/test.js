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
	'undo': {
        'width': 857.1,
        'path': 'm857 350q0-87-34-166t-91-137-137-92-166-34q-96 0-183 41t-147 114q-4 6-4 13t5 11l76 77q6 5 14 5 9-1 13-7 41-53 100-82t126-29q58 0 110 23t92 61 61 91 22 111-22 111-61 91-92 61-110 23q-55 0-105-20t-90-57l77-77q17-16 8-38-10-23-33-23h-250q-15 0-25 11t-11 25v250q0 24 22 33 22 10 39-8l72-72q60 57 137 88t159 31q87 0 166-34t137-92 91-137 34-166z',
        'ascent': 850,
        'descent': -150,
        'ascent': 850,
        'descent': -150
    }
};

layerButton = {
	name: 'Toggle Display',
	title: 'Toggle the display of the currently selected layer',
	icon: Icons.undo,
	click: function() {
		myLayer.toggleDisplay();
	}
};
document.body.appendChild(showBtn);

Plotly.newPlot(graph, [plotTrace], {title: "Is this button here?"}, {modeBarButtonsToAdd: [layerButton]});
