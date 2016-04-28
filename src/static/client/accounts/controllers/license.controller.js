app.controller('LicenseController', ['$location', '$scope', '$filter', 'LicenseFactory', function($location, $scope, $filter, LicenseFactory){

	var vm = this;
	vm.license = undefined;
	vm.updateLicense = updateLicense;

	activate();

	function activate()
	{
		LicenseFactory.get_license().then(successFn, errorFn);

		function successFn(data, status, headers, config)
		{
			console.log(data.data);
			vm.license = data.data;
			var dob = data.data.date_of_birth;

			// console.log(dob);
			dob = $filter('date')(dob, 'MM/dd/yyyy');
			// console.log(dob);
			// console.log(typeof dob);
			dob = new Date(dob);
			console.log(dob);
			vm.date_of_birth = dob;

		}

		function errorFn(data, status, headers, config)
		{
			console.error('Could not load your drivers license!');
		}
	}
	
	function updateLicense()
	{
		LicenseFactory.updateLicense(vm.license.legal_first_name, vm.license.legal_last_name, vm.license.license_id_number, vm.license.registered_city, vm.license_registered_state, vm.date_of_birth).then(successFn, errorFn);

		function successFn(data, status, headers, config)
		{
			// do something

		}

		function errorFn(data, status, headers, config)
		{
			console.error('Could not update your license!');
		}

	}


}]);