var Globals = {
  staticURL: "{{ STATIC_URL }}",
  mediaURL: "{{ MEDIA_URL }}",
  workingVIN: ""
};
$(document).ready(function() {
	//
});

tinyMCE.init({
        theme : "simple",
        mode : "textareas",
        width: "100%",
        content_css: Globals.staticURL + "css/tinymce_custom.css",
		plugins : "paste",
		paste_text_sticky : true,
		setup : function(ed) {
		    ed.onInit.add(function(ed) {
		      ed.pasteAsPlainText = true;
		    });
	  	}
});

function flagEntry(entryID, a) {
	$.post("/flag/" + entryID + "/", function(data) {
		
	}).error(function(e, jqxhr, settings, exception) {

	});
}

function yesNo(b) {
	if(b) {
		if(b == true) return "Yes";
		if(b.length == 0 || b.toLowerCase() == "unknown") return "Unknown";
		return "Yes";	
	}
	else {
		if(b == null) return "Unknown"; 
		return "No";
	}
}