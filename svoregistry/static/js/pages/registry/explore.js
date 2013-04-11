var ExploreObject = {
	jsonForSale: null,
	jsonNew: null,
	jsonSave: null,
	jsonLow: null
};

$(document).ready(function() {
	loadForSale();
	switchTab(0);
});

var loadForSale = function() {
	if(ExploreObject.jsonForSale === null) {
		$.get("/explore/forsale/", function(data) {
			ExploreObject.jsonForSale = data;
			var divContainer = document.getElementById("divForSale");
			divContainer.innerHTML = "";
			if(ExploreObject.jsonForSale) {
				if(ExploreObject.jsonForSale.length == 0) {
				}
				else {
					for(count in ExploreObject.jsonForSale) {
						var div = getCarListItem(ExploreObject.jsonForSale[count], true, false, true, false);
						divContainer.appendChild(div);
					}
				}
			}
		}).error(function(jqxhr) {
			//error
		});
	}

};

var loadNew = function(json) {
	if(ExploreObject.jsonNew === null) {
		$.get("/explore/new/", function(data) {
			ExploreObject.jsonNew = data;
			var divContainer = document.getElementById("divNew");
			divContainer.innerHTML = "";
			if(ExploreObject.jsonNew) {
				if(ExploreObject.jsonNew.length == 0) {
				}
				else {
					for(count in ExploreObject.jsonNew) {
						var div = getCarListItem(ExploreObject.jsonNew[count], false, false, true, false);
						divContainer.appendChild(div);
					}
				}
			}
		}).error(function(jqxhr) {
			//error
		});
	}
};

var loadSave = function(json) {
	if(ExploreObject.jsonSave === null) {
		$.get("/explore/save/", function(data) {
			ExploreObject.jsonSave = data;
			var divContainer = document.getElementById("divSave");
			divContainer.innerHTML = "";
			if(ExploreObject.jsonSave) {
				if(ExploreObject.jsonSave.length == 0) {
				}
				else {
					for(count in ExploreObject.jsonSave) {
						var div = getCarListItem(ExploreObject.jsonSave[count], true, false, false, false);
						divContainer.appendChild(div);
					}
				}
			}
		}).error(function(jqxhr) {
			//error
		});
	}
};

var loadLow = function(json) {
	if(ExploreObject.jsonLow === null) {
		$.get("/explore/low/", function(data) {
			ExploreObject.jsonLow = data;
			var divContainer = document.getElementById("divLow");
			divContainer.innerHTML = "";
			if(ExploreObject.jsonLow) {
				if(ExploreObject.jsonLow.length == 0) {
				}
				else {
					for(count in ExploreObject.jsonLow) {
						var div = getCarListItem(ExploreObject.jsonLow[count], true, false, false, false);
						divContainer.appendChild(div);
					}
				}
			}
		}).error(function(jqxhr) {
			//error
		});
	}
};

var switchTab = function(index) {
	var entryContainers = document.getElementsByName("container");
	var list = document.getElementById("ulTabs");
	var items = list.getElementsByTagName("li");
	var count = items.length;
	for(var i = 0; i < count; i++) {
		if(i == index) {
			items[i].className = "selectedTab";
			entryContainers[i].style.display = "";
		}
		else {
			items[i].className = "";
			entryContainers[i].style.display = "none";
		}
	}
};