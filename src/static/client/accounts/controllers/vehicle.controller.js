app.controller('VehicleController', ['$location', '$scope', 'VehicleFactory', function($location, $scope, VehicleFactory){

	var vm = this;
	vm.vehicle = undefined;

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
	


}]);