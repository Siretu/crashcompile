var guid = function() { // Deprecated. UUID is now generated server-side.
    // Taken from https://stackoverflow.com/a/2117523
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
	var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
	return v.toString(16);
    });
}



function writeCookie(name, value, days) {
    alert("Got value: "+value);
    var date, expires;
    if (days) {
        date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        expires = "; expires=" + date.toGMTString();
    }else{
        expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var i, c, ca, nameEQ = name + "=";
    ca = document.cookie.split(';');
    for(i=0;i < ca.length;i++) {
        c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return '';
}

function updateTestList() {
    var root = $("#test-list");
    console.log(root);
    console.log(nrTests);
    for (var i = 0; i < nrTests; i++) {
	var item = '<li class="list-group-item test" >Test ' + (i+1) + '<span class="glyphicon pull-right"></span></li>';
	console.log("added item");
	root.append(item);
    }
}

function updateNrTests() {
    $.get("./inc/get_tests.php",
      {id: readCookie("session")},
      function(data) {
	  nrTests = parseInt(data);
	  updateTestList();
      });
}

$(document).ready(function() {
    if (!readCookie("session")) {
	$.post("./inc/new_session.php", function(data) {
	    data = data.substring(1);
	    alert(data);
	    writeCookie("session",data);
	    updateNrTests();
	});
	alert("Wrote cookie!");
	
    } else {
	updateNrTests();
    }
    $("#probdesc").popover({
	html : true,
	title : function () {
	    return $("#probdesc-head").html();
	},
	content : function () {
	    return $("#probdesc-content").html();
	},
    });
});