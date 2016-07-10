function Layer(name, graphDiv){
	this.name = name;
	this.graphDiv = graphDiv;
	this.traces = [];
	this.hlines = [];
	this.vlines = [];
	this.bounds = [];
	this.visible = true;

	this.isEmpty(array) {
		if (typeof array !== "undefined" && array.length > 0) {
			return true;
		}
		return false;
	};

	this.isIterable = function(obj) {
		if (obj == null) {
			return false;
		}
		return (typeof obj[Symbol.iterator] === 'function') && (typeof obj === 'object');
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
				this.methodLoop(attr, methodName, iterable[val], arguments);
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
				this.propertyLoop(iterable[item], propertyName, propertyValue, arguments);
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
};

Layer.prototype.addTrace = function(trace) {
	this.traces.push(trace);
};

Layer.prototype.show = function() {
	this.visible = true;
	traceIndices = this.getTraceIndices();
	var update = {
		visible: true
	};
	if (this.graphDiv.layout.hasOwnProperty('shapes')) {
		shapeUpdate = this.graphDiv.layout.shapes;
		for (index in shapeUpdate) {
			if (shapeUpdate[index].type == 'line') {
			   shapeUpdate[index].line.width = 1;
			}	   
		}
		shapeUpdate = { shapes: shapeUpdate };
		Plotly.relayout(this.graphDiv, shapeUpdate);
	}
	Plotly.restyle(this.graphDiv, update, traceIndices);
};

Layer.prototype.hide = function() {
	this.visible = false;
	traceIndices = this.getTraceIndices();
	var update = {
		visible: false
	};
	if (this.graphDiv.layout.hasOwnProperty('shapes')) {
		shapeUpdate = this.graphDiv.layout.shapes;
		for (index in shapeUpdate) {
			if (shapeUpdate[index].type == 'line') {
				// Hiding lines by changing width to 
				// 0 is undesirably hacky. Should
				// explore better alternatives.
				shapeUpdate[index].line.width = 0;
			}	   
		}
		shapeUpdate = { shapes: shapeUpdate };
		Plotly.relayout(this.graphDiv, shapeUpdate);
	}
	Plotly.restyle(this.graphDiv, update, traceIndices);
};

Layer.prototype.safeShow = function() {
	this.visible = true;
	this.propertyLoop(this, 'visible', true);
	Plotly.redraw(this.graphDiv);
};

Layer.prototype.safeHide = function() {
	this.visible = false;
	this.propertyLoop(this, 'visible', false);
	Plotly.redraw(this.graphDiv);
};

Layer.prototype.toggleDisplay = function() {
	if (this.visible === true) {
		this.hide();
	}
	else {
		this.show();
	}
};

Layer.prototype.setProperty = function(update) {
	traceIndices = this.getTraceIndices();
	Plotly.restyle(this.graphDiv, update, traceIndices);
};

Layer.prototype.addShape = function(shape) {
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

Layer.prototype.computeAxesBounds= function() {
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

Layer.prototype.computeLayerBounds= function() {
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

Layer.prototype.addVLine = function(x) {
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

Layer.prototype.addHLine = function(y) {
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

Layer.prototype.bound = function() {
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
