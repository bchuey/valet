
var app = require('http').createServer();
var io = require('socket.io')(app);
app.listen(3000, function(){
	console.log('listening on port 3000');
});

// user adapter
var redis = require('redis');

//var store = redis.createClient();
//var pub = redis.createClient();
// var sub = redis.createClient();
var valet_client;
var valet_client1;
var user_client;


// create custom namespace for Users

var usr_nsp = io.of('/users');
var valet_nsp = io.of('/valets');
var redis_channel;

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

	socket.on('new-scheduled-repark', function(data){
		room_number = data.request_uuid;
		socket.join(room_number);
		valet_nsp.emit("incoming-scheduled-request", data);
	});

	user_client = redis.createClient();
	user_client.subscribe("users");

	user_client.on("message", function(channel, data){

		socket.emit("calculate-distance", data);
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

		// send the updated location only to User in same room
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

	// REDIS PUB/SUB

	/*
	- listen for publish from view
	- create a new socket.emit()
	- send data from view into socket.emit("",data);
	- on client side, run check if data.reparked_by == request.user
		- run socket.emit("check-matching-valet", data);

	*/
	valet_client = redis.createClient();
	valet_client1 = redis.createClient();

	// subscribe client to a channel
	valet_client.subscribe("valets");
	// listen for pub from views.py
	valet_client.on("message", function(channel, data){

		valet_nsp.emit("check-matching-valet",data);
		
	});


	// client1.subscribe("query_valets");

	// client1.on("message", function(channel,data){
	// 	valet_nsp.emit("get-current-location");
	// });


	// put valet in room for scheduled repark request
	socket.on("valet-join-room", function(data){
		room_number = data.request_uuid;
		socket.join(room_number);
		valet_nsp.to(room_number).emit("activate-directions-service", data);
	});

});







