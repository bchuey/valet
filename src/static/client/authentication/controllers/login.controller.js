
app.controller('LoginController', ['$location', '$scope', 'LoginFactory', function($location, $scope, LoginFactory){

	var vm = this;
	vm.login = login;

	function login()
	{
		LoginFactory.login(vm.email, vm.password).then(loginSuccessFn, loginErrorFn);

		function loginSuccessFn(data, status, headers, config)
		{
			// do something else when request is successful
			console.log("Successfully logged in!");
			console.log(data);
		}

		function loginErrorFn(data, status, headers, config)
		{
			console.error('Login failed!');
		};
	}

}]);
