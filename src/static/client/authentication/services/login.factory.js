app.factory('LoginFactory', ['$http', function($http){

	var LoginFactory = {
		login: login,
	};

	return LoginFactory;

	function login(email, password)
	{
		return $http.post('/login/',{
			email: email,
			password: password,
		});
	}

}]);