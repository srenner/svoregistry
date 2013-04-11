var formatShortDate = function(dt) {
	var ret = dt.toString().substring(0,10);
	var year = ret.substring(0,4);
	var month = ret.substring(5,7);
	var day = ret.substring(8,10);
	
	return month + "/" + day + "/" + year;
};

var getProblemSnippet = function getProblemSnippet(message) {
	var divProblem = document.createElement("div");
	divProblem.className = "entry-alert";
	var imgProblem = document.createElement("img");
	imgProblem.className = "entry-alert-img";
	imgProblem.src = Globals.staticURL + "img/dialog-no-3.png";
	divProblem.appendChild(imgProblem);
	var spanProblem = document.createElement("span");
	spanProblem.innerHTML = message;
	divProblem.appendChild(spanProblem);
	return divProblem;	
};

var getOwnerSnippet = function getOwnerSnippet(owner, city, state, country, zipcode) {
	var divOwner = document.createElement("div"); 
	if(!state) state = "";
	var strOwner;
	if(!owner) owner = "";
	if(owner.length == 0) {
		strOwner = "Unknown owner ";
	}
	else {
		strOwner = "Owned by " + owner;
	}
	if(city.length == 0 && state.length == 0 && country.length == 0 && zipcode.length == 0) {
		strOwner += " in unknown location";
	}
	else {
		var cityState;
		if(city.length > 0 && state.length > 0) {
			cityState = city + ", " + state;
		}
		else if(city.length == 0) {
			cityState = state;
		}
		else if(state.length == 0) {
			cityState = city;
		}
		strOwner += " in " + cityState + " " + country;
	}
	divOwner.innerHTML = strOwner;
	
	return divOwner; 
};