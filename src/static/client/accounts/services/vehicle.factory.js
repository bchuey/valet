app.factory('VehicleFactory', ['$http', function($http){

	var VehicleFactory = {

		get_vehicle: get_vehicle,
	};

	return VehicleFactory;


	function get_vehicle()
	{
		return $http.get('/accounts/dashboard/vehicle/');
	}

}]);