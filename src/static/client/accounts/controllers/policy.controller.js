app.controller('InsurancePolicyController', ['$location', '$scope', 'InsurancePolicyFactory', function($location, $scope, InsurancePolicyFactory){

	var vm = this;
	vm.policy = undefined;
	vm.updatePolicy = updatePolicy;

	activate();

	function activate()
	{
		InsurancePolicyFactory.get_policy().then(successFn, errorFn);

		function successFn(data, status, headers, config)
		{
			console.log(data.data);
			vm.policy = data.data;

		}

		function errorFn(data, status, headers, config)
		{
			console.error("Sorry, we did not find any policy on file.");
		}
	}
	
	function updatePolicy()
	{
		InsurancePolicyFactory.updatePolicy(vm.policy.company, vm.policy.policy_number, vm.policy.agent_first_name, vm.policy.agent_last_name, vm.policy.agent_phone_number).then(successFn, errorFn);

		function successFn(data, status, headers, config)
		{
			// do something
			console.log("Successfully updated your policy information.");

		}

		function errorFn(data, status, headers, config)
		{
			console.error("Sorry, we could not update your policy.");
		}

	}


}]);