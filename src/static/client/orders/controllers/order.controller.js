app.controller('UserMapController', ['$location', '$scope',  '$filter', '$ocLazyLoad', 'uiGmapGoogleMapApi', 'UserMapFactory', function($location, $scope, $filter, $ocLazyLoad, uiGmapGoogleMapApi, UserMapFactory){

	var vm = this;

	vm.socket;
	vm.map;
	vm.center_marker;
	vm.current_pos_marker;
	vm.marker_locations = [];
	vm.geocoder;
	vm.current_latitude;
	vm.current_longitude;
	vm.locked_position_lat;
	vm.locked_position_lng;
	vm.centerControlDiv;
	vm.controlUI;
	vm.controlText;
	vm.service;
	vm.user_new_position;
	
	$ocLazyLoad.load("http://127.0.0.1:3000/socket.io/socket.io.js").then(function(){
		console.log('socket.io is loaded!');
		activate();
	}, function(e) {
		console.log('error');
		console.error(e);
	});

	uiGmapGoogleMapApi.then(function(maps){

	});

	//activate();

	function activate()
	{
		console.log('runs activate function!');
		socket = io.connect('http://127.0.0.1:3000/users');
		console.log('socket is connected');
		
	}


	


}]);