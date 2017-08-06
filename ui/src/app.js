var app = angular.module('app', ['ui.router']);

app.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/home');

    $stateProvider
        // HOME STATE
        .state('home', {
            url: '/',
            templateUrl: 'components/home/home.html',
            controller: 'HomeController',
            controllerAs: 'HomeController'
        });
});