app.factory('InsurancePolicyFactory', ['$http', function($http){

	var InsurancePolicyFactory = {

		get_policy: get_policy,
		updatePolicy: updatePolicy,
	};

	return InsurancePolicyFactory;


	function get_policy()
	{
		return $http.get('/accounts/dashboard/insurance-policy/');
	}

	function updatePolicy(company, policy_number, agent_first_name, agent_last_name, agent_phone_number)
	{
		return $http.post('/accounts/dashboard/insurance-policy/', {
			company: company,
			policy_number: policy_number,
			agent_first_name: agent_first_name,
			agent_last_name: agent_last_name,
			agent_phone_number: agent_phone_number,

		});
	}

}]);

