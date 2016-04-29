app.controller('UserMapController', ['$location', '$scope',  '$filter', '$ocLazyLoad', 'uiGmapGoogleMapApi', 'UserMapFactory', function($location, $scope, $filter, $ocLazyLoad, uiGmapGoogleMapApi, UserMapFactory){

	var vm = this;
	vm.marker;
	vm.map;
	vm.lat;
    vm.lng;
    vm.error;

	$ocLazyLoad.load("http://127.0.0.1:3000/socket.io/socket.io.js").then(function(){
		console.log('socket.io is loaded!');
		activate();

		

	}, function(e) {
		console.log('error');
		console.error(e);
	});

	vm.map = {
		center: {
			latitude: 37.7082495,
			longitude: -122.44336139999999,
		},
		zoom: 15,
		events: {
			dragend: function(map, eventName, args) {
				console.log("center of map coords: " + map.getCenter().lat() + ',' + map.getCenter().lng());
				vm.marker.coords.latitude = map.center.latitude;
				vm.marker.coords.longitude = map.center.longitude;
				console.log("original marker coords: " + vm.marker.coords.latitude + ',' + vm.marker.coords.longitude);
			},
			tilesloaded: function(marker, eventName, args){

				marker.bindTo('coords', map, 'center');
			}
		},
		
	}
	vm.marker = {
		id: 0,
		coords: {
			latitude: 37.7082495,
			longitude: -122.44336139999999,
		},
		options: {
			draggable: true,
		},
		events: {
			dragend: function(marker, eventName, args) {
				var lat = marker.getPosition().lat();
				var lng = marker.getPosition().lng();
				console.log(lat, lng);
			}
		},
	}

	function activate()
	{
		console.log('runs activate function!');
		socket = io.connect('http://127.0.0.1:3000/users');
		console.log('socket is connected');


	}






}]);