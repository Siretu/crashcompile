saveFile = function() {
    var contents = editor.getSession().getValue();
    
    $.post("compile.php",
	   {contents: contents},
	   function(data) {
	       // add error checking
	       alert('successful save: ' + data);
	       $.get("read_result.php",
		     function (data2) {
			 alert("Got result: " + data2);
		     }
		    );
	   }
	  );
};


var editor = ace.edit("editor");
editor.setTheme("ace/theme/textmate");
editor.getSession().setMode("ace/mode/python");
editor.commands.addCommand({
    name: "save",
    bindKey: {
	win: "Ctrl-S",
	mac: "Command-S",
	sender: "editor|cli"
    },
    exec: function() {
	saveFile();
    }
});
