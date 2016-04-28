app.controller('UserMapController', ['$location', '$scope',  '$filter', '$ocLazyLoad', 'UserMapFactory', function($location, $scope, $filter, $ocLazyLoad, UserMapFactory){

	// $ocLazyLoad.load("http://127.0.0.1:3000/socket.io/socket.io.js").then(function() {
 //            console.log('socket.io is loaded!!');

 //        }, function(e) {
 //            console.log('errr');
 //            console.error(e);
 //    });

	$ocLazyLoad.load('/static/client/orders/controllers/testModule.js').then(function(){
		console.log('lazy load worked!');
	}, function(e) {
		console.log('error');
		console.error(e);
	});

	activate();

	function activate()
	{
		
	}

	


}]);