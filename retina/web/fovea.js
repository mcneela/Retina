function Layer(name, graphDiv){
	this.name = name;
	this.graphDiv = graphDiv;
	this.traces = [];
	this.hlines = [];
	this.vlines = [];
	this.bounds = [];
	this.x_data = [];
	this.y_data = [];
	this.visible = true;

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
	Plotly.restyle(this.graphDiv, update, traceIndices);
};

Layer.prototype.hide = function() {
	this.visible = false;
	traceIndices = this.getTraceIndices();
	var update = {
		visible: false
	};
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
