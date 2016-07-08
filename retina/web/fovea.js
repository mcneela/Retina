function Layer(name){
	this.name = name;
	this.traces = [];
	this.hlines = [];
	this.vlines = [];
	this.bounds = [];
	this.x_data = [];
	this.y_data = [];

	this.isIterable = function(obj) {
		if (obj == null) {
			return false;
		}
		return typeof obj[Symbol.iterator] === 'function';
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
			if (this.isIterable(item) === true) {
				console.log(item);
				this.propertyLoop(item, propertyName, propertyValue, arguments);
			}
			else {
				item[propertyName] = propertyValue;
			}
		}
	};
};

Layer.prototype.addTrace = function(trace) {
	this.traces.push(trace);
};

Layer.prototype.show = function() {
	this.propertyLoop(this, 'visible', true);
};

Layer.prototype.hide = function() {
	this.propertyLoop(this, 'visible', false);
};
