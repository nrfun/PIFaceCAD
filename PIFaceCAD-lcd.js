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
var exec  = require('child_process').exec;
var spawn = require('child_process').spawn;
var fs    = require('fs');

//var wrapperCommand = 'python3 ' + __dirname+'/PIFaceCAD.py';
var wrapperCommand = __dirname+'/PIFaceCAD.sh';

module.exports = function(RED) {

    
    if (!fs.existsSync("/dev/ttyAMA0")) { // unlikely if not on a Pi
        throw "Info : Ignoring Raspberry Pi specific node.";
    }

    function PIFaceLCD(config) {
        RED.nodes.createNode(this,config);
        var node = this;

        node.log("PiFaceLCD");

        var width      = config.width;
		var height     = config.height;
        var showCursor = config.showCursor;

		node.log(width + " x " + height);

        startPIFaceDriver(node);
        node.status({fill:"amber",shape:"circle",text:"ooo"});
        node.on('input', function(msg) {
            if(RED.settings.verbose) { node.log("here be some input " + msg.payload);}
        	display(node, msg.payload);
            node.status({fill:"green",shape:"circle",text:msg.payload});
        });

        
        node.on("close", function() {
            // Called when the node is shutdown - eg on redeploy.
            node.log("closing in js node" );
            stopPIFaceDriver(this);
            node.status({fill:"red",shape:"circle",text:""});
            // Allows ports to be closed, connections dropped etc.
            // eg: this.client.disconnect();
            executeCmd(node, "close");
        });


        // --- child events

        node.child.stderr.on('data', function (data) {
            if (RED.settings.verbose) { node.log("err: "+data+" :"); }
        });

        node.child.on('close', function (code) {
            if (RED.settings.verbose) { node.log("ret: "+code+" :"); }
            node.child = null;
            node.running = false;
            node.status({fill:"red",shape:"circle",text:""});
        });

        node.child.on('error', function (err) {
            if (err.errno === "ENOENT") { node.warn('Command not found'); }
            else if (err.errno === "EACCES") { node.warn('Command not executable'); }
            else { node.log('error: ' + err); }
        });

    }
    RED.nodes.registerType("PIFaceCAD-lcd",PIFaceLCD);
}


// call out to the python wrapper, but tell it to stick around
function startPIFaceDriver(node) {
    node.log("starting the 'driver'");
    node.child = spawn(wrapperCommand, ["persist"]);
}



function stopPIFaceDriver(node) {
    if (node.child != null) {
        node.child.stdin.write("close");
        node.child.kill('SIGKILL');
    }
    
    // should probably make that conditional.
    node.log("driver stopped");
}




// send the message out to the PIFaceCAD lcd module via the python process we
// started earlier
function display(node, msg) {
    console.log( "got:" + msg);
	
    // preprocess the string if we want
    //  - dimensions?
    //  - screen scrollage?

    // clear the screen
    // push the new message 
    
    if (node.child != null) {
        node.log("push the msg to the driver");
        node.child.stdin.write('disp ' + msg +  '\n');
    } else {
        executeCmd(node, "disp " + msg );
    }

} // display function

// hand off to the python process via stdio
function executeCmd(node, commandString) {
    node.log ("execute " + commandString)
    exec(wrapperCommand + " " + commandString, function(error, stdout, stderr) {
        node.log('stdout: ', stdout);
        node.log('stderr: ', stderr);
        if (error !== null) {
            console.log('exec error: ', error);
        }
    });
}


