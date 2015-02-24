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