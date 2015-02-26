function succeedTest(element) {
    element.attr("class","list-group-item list-group-item-success test");
    var glyph = element.children(":first");
    glyph.attr("class","glyphicon glyphicon-ok pull-right");
    glyph.attr("style","color:green");
}

function failTest(element) {
    element.attr("class","list-group-item list-group-item-danger test");
    var glyph = element.children(":first");
    glyph.attr("class","glyphicon glyphicon-remove pull-right");
    glyph.attr("style","color:red");    
}

function loadingTest(element) {
    element.attr("class","list-group-item test");
    var glyph = element.children(":first");
    glyph.attr("class","glyphicon glyphicon-refresh glyphicon-refresh-animate pull-right");
    glyph.removeAttr("style");
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

function messageResult(data) {
    result.setValue(data)
}

function testResult(data) {
    var i = data.testid - 1;
    var element = $(".test:eq("+i+")");
    if (data.data == "0") {
	failTest(element);
    } else {
	succeedTest(element);
    }
}

function setProblemDesc(data) {
    console.log("Setting description");
    console.log(data.head);
    console.log(data.content);
    nrTests = parseInt(data.tests);
    updateTestList();

    $("#probdesc").popover({
	html : true,
	title : function () {
	    return data.head;
	},
	content : function () {
	    return data.content;
	},
    });
    
}

var ws = new WebSocket("ws://"+window.location.hostname+":8888");

ws.onopen = function() {
    console.log("foo");
    if (!readCookie("session")) {
	ws.send(JSON.stringify({event:"init",id:""}));
    } else {
	ws.send(JSON.stringify({event:"init",id:readCookie("session")}));
    }
};

$(document).ready(function() {

    ws.onmessage = function(data) {
	var message = JSON.parse(data.data);
	console.log("Got message: " + data.data);
	if (message.id == readCookie("session")) {
	    if (message.event == "result") {
		messageResult(message.data);
	    } else if (message.event == "testresult") {
		testResult(message);
	    } else if (message.event == "problemdesc"){
		setProblemDesc(message);
	    }
	} else {
	    if (message.event == "newid") {
		writeCookie("session", message.data);
	    } else {
		console.log("ID mismatch");
	    }
	}
    };
    
});