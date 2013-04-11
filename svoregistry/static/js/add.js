function isVinValid(vin) {
	vin = vin.toUpperCase();
	if(vin.length != 17) return false;
	if(!vin.indexOf("1FABP28T") < 0) return false;
	return true;
}

function handleYear(vin, yearInputID, slapperContainerID) {
	vin = vin.toUpperCase();
	if(isVinValid(vin)) {
		var yearCode = vin[9];
		var year = "";

		switch(yearCode) {
			case "E":
				year = "1984";
				break;
			case "F":
				year = "1985";
				break;
			case "G":
				year = "1986";
				break;
			default:
				break;
		}	
		document.getElementById(yearInputID).value = year;
		setSlapperVisibility(year);
	}
}

function setSlapperVisibility(year) {
		//alert(year);
		switch(year) {
			case "1984":
				document.getElementById("spanSlappers").style.display = "";
				break;
			case "1985":
				document.getElementById("spanSlappers").style.display = "none";
				document.getElementById("spanSlappers").value = "3";
				break;
			case "1985.5":
				document.getElementById("spanSlappers").style.display = "none";
				document.getElementById("spanSlappers").value = "3";
				break;
			case "1986":
				document.getElementById("spanSlappers").style.display = "none";
				document.getElementById("spanSlappers").value = "3";
				break;
			default:
				break;
		}	
}
