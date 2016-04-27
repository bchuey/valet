app.factory('RegisterFactory', ['$http', function($http){

	var RegisterFactory = {
		register: register,
	};

	return RegisterFactory;

	function register(email, date_of_birth, first_name, last_name, password, is_valet, profile_pic)
	{
		return $http.post('/register/',{
			email: email,
			date_of_birth: date_of_birth,
			first_name: first_name,
			last_name: last_name,
			password: password,
			is_valet: is_valet,
			profile_pic: profile_pic,


		});
	}

}]);