/**
* init function: draw 10*10 tiles
* changeColor function: 
* - non, black
* - red, green
* - lighter red, lighter green
*
* 
**/
$(document).ready(function(){
	var canvas = $("#canvas")[0];
	var ctx = canvas.getContext("2d");

	var w = $("#canvas").width();
	var h = $("#canvas").height();

	var margin = 10
	var map = []

	/**
	* 0: none
	* 1: black
	* 2: red
	* 3: light red
	* 4: green
	* 5: light green
	**/

	var color = ["rgb(255, 255, 255)", "rgb(0, 0, 0)", "rgb(200, 0, 0)", "rgb(255, 0, 0)", "rgb(0, 200, 0)", "rgb(0, 255, 0)"]

	function init() {
		for (var i = 0; i < 500; i += 50) {
			var column = []
			for(var j = 0; j < 500; j += 50){
				column.push(0)
			}
			map.push(column)
		}
		for (var i = 50; i < 500; i += 50) {
			ctx.beginPath();
			ctx.fillStyle = "rgb(200, 200, 200)"
			ctx.moveTo(i,0);
			ctx.lineTo(i,500);
			ctx.stroke();
		}
		for (var i = 50; i < 500; i += 50) {
			ctx.beginPath();
			ctx.fillStyle = "rgb(200, 200, 200)"
			ctx.moveTo(0, i);
			ctx.lineTo(500, i);
			ctx.stroke();
		}
	}

	$("#canvas").click(function(e) {
		x = parseInt((e.pageX - margin) / 50);
		y = parseInt((e.pageY - margin) / 50);

		map[x][y] = (map[x][y] + 1) % 6
		ctx.strokeStyle = 'black';
		ctx.lineWidth = 1;
		ctx.strokeRect(x*50, y*50, 50, 50);
		ctx.fillStyle = color[map[x][y]]
		ctx.fillRect(x*50+1, y*50+1, 48, 48);
		
	});

	init();
});