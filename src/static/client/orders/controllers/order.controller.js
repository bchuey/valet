app.controller('UserMapController', ['$location', '$scope',  '$filter', '$ocLazyLoad', 'uiGmapGoogleMapApi', 'UserMapFactory', function($location, $scope, $filter, $ocLazyLoad, uiGmapGoogleMapApi, UserMapFactory){


	// $ocLazyLoad.load("").then(function() {
 //            console.log('google maps api is loaded!');

 //        }, function(e) {
 //            console.log('errr');
 //            console.error(e);
 //    });

	$ocLazyLoad.load("http://127.0.0.1:3000/socket.io/socket.io.js").then(function(){
		console.log('socket.io is loaded!');
	}, function(e) {
		console.log('error');
		console.error(e);
	});


	uiGmapGoogleMapApi.then(function(maps){

	});
	
	activate();

	function activate()
	{
		
	}

	


}]);