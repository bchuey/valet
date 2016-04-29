var app = angular.module('valet',['ngRoute', 'oc.lazyLoad', 'uiGmapgoogle-maps']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.config(['$httpProvider', function($httpProvider){
	
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

}]);

app.config(['uiGmapGoogleMapApiProvider', function(uiGmapGoogleMapApiProvider){
	uiGmapGoogleMapApiProvider.configure({
		key: 'AIzaSyDZWDrf4ut4695uglcR95IUHQGKQ70rHl8',
		v: '3.23',
		libraries: 'places',
	})
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
			.when('/maps/user', {
				controller: 'UserMapController',
				controllerAs: 'vm',
				templateUrl: '/static/client/orders/templates/users/map.html',
			})
			.otherwise({
				redirectTo: '/',
			});
	}]);


