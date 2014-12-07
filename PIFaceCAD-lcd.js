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


"option strict";

module.exports = function(RED) {
    function PIFaceLCD(config) {
        RED.nodes.createNode(this,config);
        var node = this;

        this.log("PiFaceLCD");

        var width      = config.width;
		var height     = config.height;
        var showCursor = config.showCursor;

		this.log(width + " x " + height);

        // Attempt to start the py child

        // handle any problems we found so far



        this.on('input', function(msg) {
        	display(msg.payload);
        });
    }
    RED.nodes.registerType("PIFaceCAD-lcd",PIFaceLCD);
}


// send the message out to the PIFaceCAD lcd module via the python process we
// started earlier
function display(msg) {
	console.log("wooo");
	
    console.log( "here:" + msg);
	
    // preprocess the string if we want
    //  - dimensions?
    //  - screen scrollage?

    // clear the screen
    // push the new message 


} // display function
