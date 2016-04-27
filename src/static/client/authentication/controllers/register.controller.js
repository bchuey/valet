

app.controller('RegisterController', ['$location', '$scope', 'RegisterFactory', function($location, $scope, RegisterFactory){

	var vm = this;
	vm.register = register;

	function register()
	{
		RegisterFactory.register(vm.email, vm.date_of_birth, vm.first_name, vm.last_name, vm.password, vm.is_valet, vm.profile_pic).then(registerSuccessFn, registerErrorFn);

		function registerSuccessFn(data, status, headers, config)
		{
			// do something else when request is successful
			console.log("Successfully registered!");
		}

		function registerErrorFn(data, status, headers, config)
		{
			console.error('Registration failed!');
		};
	}

}]);
