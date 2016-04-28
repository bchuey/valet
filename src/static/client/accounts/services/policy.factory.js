app.factory('InsurancePolicyFactory', ['$http', function($http){

	var InsurancePolicyFactory = {

		get_policy: get_policy,
	};

	return InsurancePolicyFactory;


	function get_policy()
	{
		return $http.get('/accounts/dashboard/insurance-policy/');
	}

}]);