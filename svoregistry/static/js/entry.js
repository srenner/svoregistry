function deNull(val, ifNullVal) {
	if(val == null) {
		if(ifNullVal) return ifNullVal;
		else return "";
	}
	else return val;
}
function getEntryDiv(entry) {
	//debugger;
	var entryID = entry.pk;
	var city = deNull(entry.fields.city);
	var optionDelete = entry.fields.option_delete;
	var mileage = entry.fields.mileage;
	var photoURL = entry.fields.photo;
	var wingDelete = entry.fields.wing_delete;
	var slappers = entry.fields.slappers;
	var color = deNull(entry.fields.color, "Unknown or custom");
	var country = deNull(entry.fields.country);
	var sunroof = deNull(entry.fields.sunroof, "Unknown");
	var zipcode = deNull(entry.fields.zipcode);
	var owner = entry.fields.owner;
	var has23 = deNull(entry.fields.has_23, true);
	var compPrep = entry.fields.comp_prep;
	var state = deNull(entry.fields.state);
	var onRoad = deNull(entry.fields.on_road, true);
	var comments = entry.fields.comments;
	var year = deNull(entry.fields.year, "Unknown year");
	var interior = deNull(entry.fields.interior, "Unknown");
	var entryDate = entry.fields.entry_datetime;
	var deceased = entry.fields.deceased;
	try {
		entryDate = new Date(entryDate).toDateString();
	}
	catch(e) {
		entryDate = entry.fields.entry_datetime.toString().substring(0,10);
	}
	if(entryDate == "NaN") {
		entryDate = entry.fields.entry_datetime.toString().substring(0,10);
	}
	var divEntry = document.createElement("div");
	divEntry.className = "entry";
	if(photoURL && photoURL.length > 0) {
		var divPhoto = document.createElement("div");
		divPhoto.className = "center";
		var photo = document.createElement("img");
		photo.src = Globals.mediaURL + photoURL;
		divPhoto.appendChild(photo);
		divEntry.appendChild(divPhoto);
	}
	var h3Car = document.createElement("h3");
	if(!mileage) {
		mileage = "unknown";
	}
	else {
		mileage = mileage.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}
	h3Car.innerHTML = year + " SVO with " + mileage + " miles. Entered " + entryDate + ".";
	divEntry.appendChild(h3Car);
	var divCar = document.createElement("div");
	if(!onRoad) {
		var deadMessage = "This SVO is not on the road, but may be fixable";
		if(deceased) {
			deadMessage = "This SVO is listed as deceased";
		}
		var divDead = document.createElement("div");
		divDead.className = "entry-alert";
		var imgDead = document.createElement("img");
		imgDead.className = "entry-alert-img";
		imgDead.src = Globals.staticURL + "img/dialog-no-3.png";
		divDead.appendChild(imgDead);
		var spanDead = document.createElement("span");
		spanDead.innerHTML = deadMessage;
		divDead.appendChild(spanDead);
		divCar.appendChild(divDead);
	}
	if(!has23) {
		var divEngine = getProblemSnippet("This SVO no longer has the 2.3L engine");
		divCar.appendChild(divEngine);
	}
	if(slappers) {
		var divSlappers = document.createElement("div");
		divSlappers.className = "entry-alert";
		var imgSlappers = document.createElement("img");
		imgSlappers.src = Globals.staticURL + "img/dialog-yes.png";
		divSlappers.appendChild(imgSlappers);
		var spanSlappers = document.createElement("span");
		spanSlappers.innerHTML = "Slapper bars";
		divSlappers.appendChild(spanSlappers);
		divCar.appendChild(divSlappers);
	}
	if(compPrep) {
		var divCompPrep = document.createElement("div");
		divCompPrep.className = "entry-alert";
		var imgCompPrep = document.createElement("img");
		imgCompPrep.src = Globals.staticURL + "img/dialog-yes.png";
		divCompPrep.appendChild(imgCompPrep);
		var spanCompPrep = document.createElement("span");
		spanCompPrep.innerHTML = "Competition prep";
		divCompPrep.appendChild(spanCompPrep);
		divCar.appendChild(divCompPrep);
	}
	else if(optionDelete) {
		var divOptionDelete = document.createElement("div");
		divOptionDelete.className = "entry-alert";
		var imgOptionDelete = document.createElement("img");
		imgOptionDelete.src = Globals.staticURL + "img/dialog-yes.png";
		divOptionDelete.appendChild(imgOptionDelete);
		var spanOptionDelete = document.createElement("span");
		spanOptionDelete.innerHTML = "Option delete";
		divOptionDelete.appendChild(spanOptionDelete);
		divCar.appendChild(divOptionDelete);		
	}
	if(wingDelete) {
		var divWingDelete = document.createElement("div");
		divWingDelete.className = "entry-alert";
		var imgWingDelete = document.createElement("img");
		imgWingDelete.src = Globals.staticURL + "img/dialog-yes.png";
		divWingDelete.appendChild(imgWingDelete);
		var spanWingDelete = document.createElement("span");
		spanWingDelete.innerHTML = "Bi-wing delete";
		divWingDelete.appendChild(spanWingDelete);
		divCar.appendChild(divWingDelete);
	}
	if(!slappers && !compPrep && !optionDelete && !wingDelete) {
		var divNotSpecial = document.createElement("div");
		divNotSpecial.className = "entry-alert";
		var imgNotSpecial = document.createElement("img");
		imgNotSpecial.src = Globals.staticURL + "img/dialog-yes.png";
		divNotSpecial.appendChild(imgNotSpecial);
		var spanNotSpecial = document.createElement("span");
		spanNotSpecial.innerHTML = "This SVO does not have any uncommon factory options";
		divNotSpecial.appendChild(spanNotSpecial);
		divCar.appendChild(divNotSpecial);		
	}
	var divOptions = document.createElement("div");
	var spanColor = document.createElement("span");
	spanColor.innerHTML = "Color: " + color;
	spanColor.style.marginRight = "25px";
	divOptions.appendChild(spanColor);
	var spanInterior = document.createElement("span");
	spanInterior.innerHTML = "Interior: " + interior;
	spanInterior.style.marginRight = "25px";
	divOptions.appendChild(spanInterior);
	var spanSunroof = document.createElement("span");
	spanSunroof.innerHTML = "Sunroof: " + yesNo(sunroof);
	divOptions.appendChild(spanSunroof);
	divCar.appendChild(divOptions);
	divEntry.appendChild(divCar);
	var h3Owner = document.createElement("h3");
	h3Owner.innerHTML = "Owner Info";
	divEntry.appendChild(h3Owner);
	var divOwner = getOwnerSnippet(owner, city, state, country, zipcode);
	divEntry.appendChild(divOwner);
	if(comments.length > 0) {
		var h3Comments = document.createElement("h3");
		h3Comments.innerHTML = "Comments";
		divEntry.appendChild(h3Comments);
		var divComments = document.createElement("div");
		divComments.innerHTML = comments;
		divEntry.appendChild(divComments);
	}
	var divFlag = document.createElement("div");
	divFlag.style.textAlign = "right";
	divFlag.style.fontSize = "10pt";
	divFlag.style.marginTop = "15px";
	var aFlag = document.createElement("a");
	aFlag.href = "javascript:flagEntry(" + entryID + ",this)";
	var spanFlag = document.createElement("span");
	spanFlag.innerHTML = "Flag this entry as inappropriate or not an SVO";
	var imgFlag = document.createElement("img");
	imgFlag.style.border = "0";
	imgFlag.src =  Globals.staticURL + "img/flag-red.png";
	imgFlag.style.marginBottom = "-2px";
	aFlag.appendChild(imgFlag);
	aFlag.appendChild(spanFlag);
	divFlag.appendChild(aFlag);
	divEntry.appendChild(divFlag);
	return divEntry;
}