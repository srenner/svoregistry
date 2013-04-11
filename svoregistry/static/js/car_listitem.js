var getCarListItem = function getCarListItem(obj, viewProblems, viewOptions, viewOwner, viewThumbnail) {
	var divContainer = document.createElement("div");
	divContainer.className = "carListItem";
	var divItem = document.createElement("div");
	var model = obj.model;
	var vin;
	var year;
	var has23;
	var onRoad;
	var deceased;
	if(model === "registry.car") {
		vin = obj.pk;
	}
	else if(model === "registry.entry") {
		vin = obj.fields.car;
	}
	year = obj.fields.year;
	has23 = obj.fields.has_23;
	onRoad = obj.fields.on_road;
	deceased = obj.fields.deceased;
	divItem.title = "Click to view car " + vin;
	var divLine1 = document.createElement("div");
	
	divLine1.style.fontSize = "18pt";
	divLine1.style.fontWeight = "bold";
	divLine1.style.marginBottom = "2px";
	divLine1.innerHTML =  vin + " - " + year + " SVO";
	divItem.appendChild(divLine1);
	
	var divIndent = document.createElement("div");
	divIndent.className = "carListItemIndent";
	
	if(viewProblems) {
		var divProblems = document.createElement("div");
		if(!has23) {
			var div23 = getProblemSnippet("This SVO no longer has the 2.3L engine");
			divIndent.appendChild(div23);
		}
		if(!onRoad) {
			var divDead = getProblemSnippet("This SVO is not on the road, but may be fixable");
			divIndent.appendChild(divDead);
		}

	}
	if(viewOptions) {
		
	}
	if(viewOwner) {
		var owner = nullToString(obj.fields.owner);
		var city = nullToString(obj.fields.city);
		var state = nullToString(obj.fields.state);
		var country = nullToString(obj.fields.country);
		var zipcode = nullToString(obj.fields.zipcode);
		var divOwner = getOwnerSnippet(owner, city, state, country, zipcode);
		divIndent.appendChild(divOwner);
	}
	if(viewThumbnail) {
		//not implemented
	}
	
	divItem.appendChild(divIndent);
		
	var a = document.createElement("a");
	a.href = "/" + vin + "/";
	a.appendChild(divItem);
	
	divContainer.appendChild(a);
	
	return divContainer;
};

var nullToString = function(val) {
	if(!val) {
		return '';
	}
	else {
		return val;
	}
};
