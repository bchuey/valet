app.factory('LicenseFactory', ['$http', function($http){

	var LicenseFactory = {

		get_license: get_license,
	};

	return LicenseFactory;


	function get_license()
	{
		return $http.get('/accounts/dashboard/license/');
	}

}]);