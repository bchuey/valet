app.controller('InsurancePolicyController', ['$location', '$scope', 'InsurancePolicyFactory', function($location, $scope, InsurancePolicyFactory){

	var vm = this;
	vm.policy = undefined;

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
	


}]);