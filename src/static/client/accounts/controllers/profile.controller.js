app.controller('ProfileController', ['$location', '$scope',  '$filter', 'ProfileFactory', function($location, $scope, $filter, ProfileFactory){

	var vm = this;
	vm.user = undefined;

	activate();

	function activate()
	{
		ProfileFactory.get_profile().then(successFn, errorFn);

		function successFn(data, status, headers, config)
		{
			console.log(data.data);
			vm.user = data.data;
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
			console.error('Could not load profile!');
		}
	}
	


}]);