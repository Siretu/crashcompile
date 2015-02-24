/*function loadResult () {
    console.log("Loading");
    // add error checking ?
    $.get("inc/read_result.php",
	  {id: readCookie("session")},
	  function (data) {
	      result.setValue(data,1);
	  });
};

function runCode (callback) {
    console.log("Running");
    // Add some kind of hashing to see if it has changed since last save?
    $.post("inc/run_code.php",
	   {id: readCookie("session")},
	   function(data) {
	       console.log(data);
	       if (callback) {
		   callback();
	       }
	   }
	  );
    
};

function saveFile(callback) {
    console.log("Saving");
    var contents = editor.getSession().getValue();
    $.post("inc/compile.php",
	   {contents: contents,
	    id: readCookie("session")},
	   callback
	  );
};
*/


function testCode () {
    console.log("Testing");
    for (var i = 0; i < nrTests; i++) {
	var element = $(".test:eq("+i+")")
	loadingTest(element);
    }
    var message = {event: "test", data: editor.getSession().getValue(), id: readCookie("session")};
    ws.send(JSON.stringify(message));
};



var editor = ace.edit("editor");
var editor_div = document.getElementById('editor');
var doc = editor.getSession().getDocument()

editor.on('change', function() {
    // assuming a line height of 16 pixels
    editor_div.style.height = 16 * doc.getLength() + 'px';
    editor.resize();
});

editor.setTheme("ace/theme/textmate");
editor.getSession().setMode("ace/mode/python");
editor.commands.addCommand({
    name: "save",
    bindKey: {
	win: "Ctrl-S",
	mac: "Ctrl-S",
	sender: "editor|cli"
    },
    exec: function() {
	var message = {event: "run",data: editor.getSession().getValue(), id: readCookie("session")};
	ws.send(JSON.stringify(message));
	//saveFile(runCode(loadResult));
    }
});
editor.commands.addCommand({
    name: "test",
    bindKey: {
	win: "Ctrl-D",
	mac: "Ctrl-D",
	sender: "editor|cli"
    },
    exec: function() {
	testCode();
    }
});
$("#editor_box").mousedown(function() {
    editor.focus();
});

var result = ace.edit("result");
result.setTheme("ace/theme/terminal");
result.getSession().setMode("ace/mode/python");
result.setReadOnly(true);