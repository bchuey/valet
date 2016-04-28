app.factory('VehicleFactory', ['$http', function($http){

	var VehicleFactory = {

		get_vehicle: get_vehicle,
		updateVehicle: updateVehicle,
	};

	return VehicleFactory;


	function get_vehicle()
	{
		return $http.get('/accounts/dashboard/vehicle/');
	}

	function updateVehicle(make, model, color, year, license_plate_number, updated_registration_tags, parking_permit_zone)
	{
		return $http.post('/accounts/dashboard/vehicle/', {
			make: make,
			model: model,
			color: color,
			year: year,
			license_plate_number: license_plate_number,
			updated_registration_tags: updated_registration_tags,
			parking_permit_zone: parking_permit_zone,
		});

	}

}]);