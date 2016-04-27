app.factory('ProfileFactory', ['$http', function($http){

	var ProfileFactory = {

		get_profile: get_profile,
	};

	return ProfileFactory;


	function get_profile()
	{
		return $http.get('/accounts/dashboard/profile/');
	}

}]);