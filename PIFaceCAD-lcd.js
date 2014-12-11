// PIFaceCAD-lcd.js
// First stab at something to noderedify the PIFaceCAD display
// cwhite
// December 2014
// See if we can live with pythonic 'driver' for now, using node child process thing
// For now just dump the whole message out there

// Future:
//  - scrolling
//  - update regions - param the region location and sizes
//  - flash the back light
//  - custom characters
//  - config of cursor modes


"option strict";
var exec = require('child_process').exec;
var fs   = require('fs');
var wrapperCommand = 'python3 ' + __dirname+'/PIFaceCAD.py';

module.exports = function(RED) {

    
    if (!fs.existsSync("/dev/ttyAMA0")) { // unlikely if not on a Pi
        throw "Info : Ignoring Raspberry Pi specific node.";
    }

    function PIFaceLCD(config) {
        RED.nodes.createNode(this,config);
        var node = this;

        this.log("PiFaceLCD");

        var width      = config.width;
		var height     = config.height;
        var showCursor = config.showCursor;

		this.log(width + " x " + height);

        this.on('input', function(msg) {
            this.log("here be some input " + msg.payload);
        	display(msg.payload);
        });

        
        this.on("close", function() {
            // Called when the node is shutdown - eg on redeploy.
            this.log("closing in js node" );
            // Allows ports to be closed, connections dropped etc.
            // eg: this.client.disconnect();
            executeCmd("close");
        });

    }
    RED.nodes.registerType("PIFaceCAD-lcd",PIFaceLCD);
}

// send the message out to the PIFaceCAD lcd module via the python process we
// started earlier
function display(msg) {
    console.log( "got:" + msg);
	
    // preprocess the string if we want
    //  - dimensions?
    //  - screen scrollage?

    // clear the screen
    // push the new message 
    executeCmd("disp '" + msg + "'")

} // display function

// hand off to the python process via stdio
function executeCmd(commandString) {
    console.log ("execute " + commandString)
    exec(wrapperCommand + " " + commandString, function(error, stdout, stderr) {
        console.log('stdout: ', stdout);
        console.log('stderr: ', stderr);
        if (error !== null) {
            console.log('exec error: ', error);
        }
    });
}


