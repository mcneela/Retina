function Layer2D(name, graphDiv) {
	this.name = name;
	this.graphDiv = graphDiv;
	this.traces = [];
	this.hlines = [];
	this.vlines = [];
	this.bounds = [];
	this.visible = true;

	this.firstLayer = function() {
		if (document.getElementById('layerButton')) {
			this.first = false;
			return false;
		}
		this.first = true;
		return true;
	}

	this.isEmpty = function(array) {
		if (typeof array !== "undefined"
			   	&& array.length > 0) {
			return true;
		}
		return false;
	};

	this.isIterable = function(obj) {
		if (obj == null) {
			return false;
		}
		return (typeof obj[Symbol.iterator] === 'function')
		   	&& (typeof obj === 'object');
	};

	this.tryMethod = function(val, methodName) {
		try {
			methodName(val, arguments);
		}
		catch(error) {}
	};
	
	this.attrTryMethod = function(val, methodName) {
		try {
			val[methodName](arguments);
		}
		catch(error) {}
	};

	this.methodLoop = function(attr, methodName, iterable) {
		for (var val in iterable) {
			if (this.isIterable(iterable[val]) === true) {
				this.methodLoop(attr, methodName,
					   	iterable[val], arguments);
			}
			else {
				if (attr === true) {
					this.attrTryMethod(val, methodName, arguments);
				}
				else {
					this.tryMethod(val, methodName, arguments);
				}
			}
		}
	};

	this.propertyLoop = function(iterable, propertyName, propertyValue) {
		for (var item in iterable) {
			if (this.isIterable(iterable[item]) === true) {
				this.propertyLoop(iterable[item], propertyName,
					   		      propertyValue, arguments);
			}
			else {
				iterable[item][propertyName] = propertyValue;
			}
		}
	};

	this.getTraceIndices = function() {
		indices = [];
		for (var trace in this.traces) {
			var index = this.graphDiv.data.indexOf(this.traces[trace]);
			indices.push(index);
		}
		return indices;
	};

	this.addToUI();

	this.manager = new LayerManager(this);
};

Layer2D.prototype.addTrace = function(trace) {
	this.traces.push(trace);
};

Layer2D.prototype.shapeVisible = function(arr, bool) {
	if (this.graphDiv.layout.hasOwnProperty('shapes')) {
		shapeUpdate = this.graphDiv._fullLayout.shapes;
		for (index in shapeUpdate) {
			if (arr.indexOf(shapeUpdate[index]) >= 0) {
				shapeUpdate[index].line.visible = bool;
			}	   
		}
		shapeUpdate = { shapes: shapeUpdate };
		Plotly.relayout(this.graphDiv, shapeUpdate);
	}
};

Layer2D.prototype.show = function() {
	this.visible = true;
	traceIndices = this.getTraceIndices();
	var update = {
		visible: true
	};
	this.shapeVisible(this.hlines, true);
	this.shapeVisible(this.vlines, true);
	this.shapeVisible(this.bounds, true);
	Plotly.restyle(this.graphDiv, update, traceIndices);
};

Layer2D.prototype.hide = function() {
	this.visible = false;
	traceIndices = this.getTraceIndices();
	var update = {
		visible: false
	};
	this.shapeVisible(this.hlines, false);
	this.shapeVisible(this.vlines, false);
	this.shapeVisible(this.bounds, false);
	Plotly.restyle(this.graphDiv, update, traceIndices);
};

Layer2D.prototype.safeShow = function() {
	this.visible = true;
	this.propertyLoop(this, 'visible', true);
	Plotly.redraw(this.graphDiv);
};

Layer2D.prototype.safeHide = function() {
	this.visible = false;
	this.propertyLoop(this, 'visible', false);
	Plotly.redraw(this.graphDiv);
};

Layer2D.prototype.toggleDisplay = function() {
	if (this.visible === true) {
		this.hide();
	}
	else {
		this.show();
	}
};

Layer2D.prototype.setProperty = function(update) {
	traceIndices = this.getTraceIndices();
	Plotly.restyle(this.graphDiv, update, traceIndices);
};

Layer2D.prototype.addShape = function(shape) {
	if (this.graphDiv.layout.hasOwnProperty('shapes')) {
		plotShapes = this.graphDiv.layout.shapes;
		plotShapes.push(shape);
		plotShapes = {shapes: plotShapes};
	}
	else {
		plotShapes = {shapes: [shape]};
	}	
	Plotly.relayout(this.graphDiv, plotShapes);
}

Layer2D.prototype.computeAxesBounds= function() {
	var xMax = Math.max.apply(Math, this.graphDiv.data[0].x);
	var xMin = Math.min.apply(Math, this.graphDiv.data[0].x);
	var yMax = Math.max.apply(Math, this.graphDiv.data[0].y);
	var yMin = Math.min.apply(Math, this.graphDiv.data[0].y);
	for (var index in this.graphDiv.data) {
		var traceXMax = Math.max.apply(Math, this.graphDiv.data[index].x);
		var traceXMin = Math.min.apply(Math, this.graphDiv.data[index].x);
		var traceYMax = Math.max.apply(Math, this.graphDiv.data[index].y);
		var traceYMin = Math.min.apply(Math, this.graphDiv.data[index].y);
		if (traceXMax > xMax) {
			xMax = traceXMax;
		}
		if (traceXMin < xMin) {
			xMin = traceXMin;
		}
		if (traceYMax > yMax) {
			yMax = traceYMax;
		}
		if (traceYMin < yMin) {
			yMin = traceYMin;
		}
	}
	return [xMin, xMax, yMin, yMax];
};

Layer2D.prototype.computeLayerBounds= function() {
	var xMax = Math.max.apply(Math, this.traces[0].x);
	var xMin = Math.min.apply(Math, this.traces[0].x);
	var yMax = Math.max.apply(Math, this.traces[0].y);
	var yMin = Math.min.apply(Math, this.traces[0].y);
	for (var index in this.traces) {
		var traceXMax = Math.max.apply(Math, this.traces[index].x);
		var traceXMin = Math.min.apply(Math, this.traces[index].x);
		var traceYMax = Math.max.apply(Math, this.traces[index].y);
		var traceYMin = Math.min.apply(Math, this.traces[index].y);
		if (traceXMax > xMax) {
			xMax = traceXMax;
		}
		if (traceXMin < xMin) {
			xMin = traceXMin;
		}
		if (traceYMax > yMax) {
			yMax = traceYMax;
		}
		if (traceYMin < yMin) {
			yMin = traceYMin;
		}
	}
	return [xMin, xMax, yMin, yMax];
};

Layer2D.prototype.addVLine = function(x) {
	[xMin, xMax, yMin, yMax] = this.computeAxesBounds();
	vLine = {
				type: 'line',
				x0: x,
				y0: yMin,
				x1: x,
				y1: yMax,
				line: {
					color: 'rgb(0, 0, 0)',
					width: 1,
				}
			};

	this.vlines.push(vLine);
	this.addShape(vLine);
};

Layer2D.prototype.addHLine = function(y) {
	[xMin, xMax, yMin, yMax] = this.computeAxesBounds();
	hLine = {
				type: 'line',
				x0: xMin,
				y0: y,
				x1: xMax,
				y1: y,
				line: {
					color: 'rgb(0, 0, 0)',
					width: 1
				}
			};

	this.hlines.push(hLine);
	this.addShape(hLine);
};

Layer2D.prototype.bound = function() {
	[xMin, xMax, yMin, yMax] = this.computeLayerBounds();

	var rectangle = {
						type: 'rect',
						x0: xMin,
						y0: yMin,
						x1: xMax,
						y1: yMax,
						line: {
							color: 'rgba(0, 0, 0)',
							width: 1
						}
	};
	this.bounds.push(rectangle);	
this.addShape(rectangle);
};

Layer2D.prototype.clear = function() {
	traceIndices = this.getTraceIndices();
	Plotly.deleteTraces(this.graphDiv, traceIndices);
	Plotly.redraw(this.graphDiv);
};

Layer2D.prototype.addToUI = function() {
	if (this.firstLayer()) {
		var layerDiv = document.createElement('div');
		layerDiv.className = 'content';
		layerDiv.id = 'layerNames';
	}
	else {
		var layerDiv = document.getElementById('layerNames');
	}

	layerDiv.innerHTML += '</br>' +
						  '<div class="ui toggle mini checkbox" id="layer' + this.name +'">' +
						  '<input type="checkbox" name="' + this.name + '" checked>' +
						  '</input>' +
						  '<label>' + this.name + '</label>' +
						  '</div>';

	if (this.firstLayer()) {
		var parentDiv = document.getElementById('layerMenu');
		parentDiv.appendChild(layerDiv);
	};
	$('#layer' + this.name).after('<br/>');

	var This = this;
	$(document).on('click', '#layer' + this.name + ' :input', function() {
		checked = $(this).is(':checked');
		console.log(This);
		if (checked === true) {
			This.show();
		}
		else { 
			This.hide();
		}
	});

	var jsonDiv = $('#jsonDropdown .menu');
	jsonDiv.append('<div class="item" data-value="' + this.name + '">' + this.name + '</div>')
};

function Layer3D(name, graphDiv) {
	Layer2D.call(this, name, graphDiv);
};

Layer3D.prototype = Object.create(Layer2D.prototype);

Layer3D.prototype.computeLayerBounds= function() {
	var xMax = Math.max.apply(Math, this.traces[0].x);
	var xMin = Math.min.apply(Math, this.traces[0].x);
	var yMax = Math.max.apply(Math, this.traces[0].y);
	var yMin = Math.min.apply(Math, this.traces[0].y);
	var zMax = Math.max.apply(Math, this.traces[0].z);
	var zMin = Math.min.apply(Math, this.traces[0].z);

	for (var index in this.traces) {
		var traceXMax = Math.max.apply(Math, this.traces[index].x);
		var traceXMin = Math.min.apply(Math, this.traces[index].x);
		var traceYMax = Math.max.apply(Math, this.traces[index].y);
		var traceYMin = Math.min.apply(Math, this.traces[index].y);
		var traceZMax = Math.max.apply(Math, this.traces[index].z);
		var traceZMin = Math.min.apply(Math, this.traces[index].z);
		if (traceXMax > xMax) {
			xMax = traceXMax;
		}
		if (traceXMin < xMin) {
			xMin = traceXMin;
		}
		if (traceYMax > yMax) {
			yMax = traceYMax;
		}
		if (traceYMin < yMin) {
			yMin = traceYMin;
		}
		if (traceZMin < zMin) {
			zMin = traceZMin;
		}
		if (traceZMax > zMax) {
			xMax = traceZMax;
		}
	}
	return [xMin, xMax, yMin, yMax, zMin, zMax];
};	

Layer3D.prototype.cartesianProduct = function(array) {
    return array.reduce(function(a,b) {
        return a.map(function(x) {
            return b.map(function(y) {
                return x.concat(y);
            })
        }).reduce(function(a,b){ return a.concat(b) }, [])
    }, [[]])
};	

Layer3D.prototype.bound = function() {
	[xMin, xMax, yMin, yMax, zMin, zMax] = this.computeLayerBounds();
	var x = [xMin, xMax];
	var y = [yMin, yMax];
	var z = [zMin, zMax];
	
	var corners = this.cartesianProduct([x, y, z]);
	
	var xVals = corners.map(function(value, index) { return value[0] });
	var yVals = corners.map(function(value, index) { return value[1] });
	var zVals = corners.map(function(value, index) { return value[2] });

	var box = {
				type: 'scatter3d',
				mode: 'lines',
				x: xVals,
				y: yVals,
				z: zVals,
				line: {
					color: 'rgba(0, 0, 0)',
					width: 1
				}
	};
	this.bounds.push(box);	
	this.traces.push(box);
	Plotly.addTraces(this.graphDiv, box);
};

function LayerManager(layer) {
	this.layer = layer;
	if (layer.first) {
		var parentDiv = document.getElementById('layerNames');
		this.layerButton = document.createElement('button');
		this.layerButton.className = 'ui mini button';
		this.layerButton.id = 'layerButton';
		this.layerButton.textContent = 'Open Layer Manager';
		var lineBreak = document.createElement('br');
		parentDiv.insertBefore(lineBreak, parentDiv.firstChild);
		parentDiv.insertBefore(this.layerButton, parentDiv.firstChild);
	}
	
}

//LayerManager.bindClick();

//exports.Layer2D = Layer2D;
//exports.Layer3D = Layer3D;
