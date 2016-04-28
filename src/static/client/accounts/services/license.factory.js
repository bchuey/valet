app.factory('LicenseFactory', ['$http', function($http){

	var LicenseFactory = {

		get_license: get_license,
	};

	return LicenseFactory;


	function get_license()
	{
		return $http.get('/accounts/dashboard/license/');
	}

	function updateLicense(legal_first_name, legal_last_name, date_of_birth, license_id_number, registered_city, registered_state)
	{
		return $http.post('/accounts/dashboard/license/', {
			legal_first_name: legal_first_name,
			legal_last_name: legal_last_name,
			date_of_birth: date_of_birth,
			license_id_number: license_id_number,
			registered_city: registered_city,
			registered_state: registered_state,
			
		});
	}

}]);