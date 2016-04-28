app.factory('ProfileFactory', ['$http', function($http){

	var ProfileFactory = {

		get_profile: get_profile,
		updateProfile: updateProfile,
	};

	return ProfileFactory;


	function get_profile()
	{
		return $http.get('/accounts/dashboard/profile/');
	}

	function updateProfile(email, first_name, last_name, date_of_birth)
	{
		return $http.post('/accounts/dashboard/profile/', {
			email: email,
			first_name: first_name,
			last_name: last_name,
			date_of_birth: date_of_birth,

		});
	}


}]);