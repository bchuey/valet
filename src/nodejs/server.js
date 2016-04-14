
var app = require('http').createServer();
var io = require('socket.io')(app);
app.listen(3000, function(){
	console.log('listening on port 3000');
});

var redis = require('socket.io/node_modules/redis');


// create custom namespace for Users

var usr_nsp = io.of('/users');
var valet_nsp = io.of('/valets');

usr_nsp.on('connection', function(socket){
	console.log('user has connected to /users namespace');
	var room_number;

	socket.on('request-valet', function(data){

		console.log("listening for request valet");
		console.log(data);
		valet_nsp.emit("incoming-request", data);
		room_number = data.request_uuid;
		socket.join(room_number);



	});


});


valet_nsp.on('connection', function(socket){
	console.log('valet has connected to /valets namespace');

	var room_number;

	socket.on('join-room', function(data){
		// assign valet to room
		console.log("valet is joining room");
		console.log(data);
		room_number = data.request_uuid;
		// var lat = data.lat;
		// var lng = data.lng;
		socket.join(room_number);

		// signal to tell other valet screens to remove 'floating-request-screen' and 'button' 

		// valet_nsp.emit("valet-assigned-to-request");
		socket.broadcast.emit("valet-assigned-to-request");

		usr_nsp.to(room_number).emit("request-accepted", data);
		valet_nsp.to(room_number).emit("activate-directions-service", data);
	});


	socket.on('get-new-location', function(data){

		// send the updated location only to User
		// maybe use .broadcast??
		usr_nsp.to(room_number).emit("update-valet-location", data);

	});

	socket.on("valet-arrived", function(){

		usr_nsp.to(room_number).emit("alert-valet-arrived");

	});

	socket.on("valet-enroute", function(){
		usr_nsp.to(room_number).emit("alert-valet-enroute");
	});

	socket.on("vehicle-reparked", function(data){
		usr_nsp.to(room_number).emit("vehicle-new-location",data);
	})

	socket.on("request-completed", function(){
		usr_nsp.to(room_number).emit("requested-repark-completed");
	})

});



