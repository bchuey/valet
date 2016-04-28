app.controller('VehicleController', ['$location', '$scope', 'VehicleFactory', function($location, $scope, VehicleFactory){

	var vm = this;
	vm.vehicle = undefined;
	vm.updateVehicle = updateVehicle;

	activate();

	function activate()
	{
		VehicleFactory.get_vehicle().then(successFn, errorFn);

		function successFn(data, status, headers, config)
		{
			console.log(data.data);
			vm.vehicle = data.data;

		}

		function errorFn(data, status, headers, config)
		{
			console.error('Could not load your registered vehicle!');
		}
	}

	function updateVehicle()
	{
		VehicleFactory.updateVehicle(vm.vehicle.make, vm.vehicle.model, vm.vehicle.year, vm.vehicle.color, vm.vehicle.license_plate_number, vm.vehicle.updated_registration_tags, vm.vehicle.parking_permit_zone).then(successFn, errorFn);

		function successFn(data, status, headers, config)
		{
			console.log(data.data);

		}

		function errorFn(data, status, headers, config)
		{
			console.error('Could not update your vehicle information!');
		}
	}
	


}]);