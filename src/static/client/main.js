var app = angular.module('valet',['ngRoute']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.config(['$httpProvider', function($httpProvider){
	

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

}]);

app.config(['$routeProvider',
	function($routeProvider){
		$routeProvider
			.when('/', {
				controller: '',
				controllerAs: '',
				templateUrl: '/static/client/index.html',
			})
			.when('/login', {
				controller: 'LoginController',
				controllerAs: 'vm',
				templateUrl: '/static/client/authentication/templates/login.html',

			})
			.when('/register', {
				controller: 'RegisterController',
				controllerAs: 'vm',
				templateUrl: '/static/client/authentication/templates/register.html',

			})
			.when('/dashboard/profile', {
				controller: 'ProfileController',
				controllerAs: 'vm',
				templateUrl: '/static/client/accounts/templates/profile.html',
			})
			.when('/dashboard/vehicle', {
				controller: 'VehicleController',
				controllerAs: 'vm',
				templateUrl: '/static/client/accounts/templates/vehicle.html',
			})
			.when('/dashboard/license', {
				controller: 'LicenseController',
				controllerAs: 'vm',
				templateUrl: '/static/client/accounts/templates/license.html',
			})
			.when('/dashboard/insurance', {
				controller: 'InsurancePolicyController',
				controllerAs: 'vm',
				templateUrl: '/static/client/accounts/templates/insurance_policy.html',
			})
			.otherwise({
				redirectTo: '/',
			});
	}]);


