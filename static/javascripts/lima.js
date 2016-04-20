(function(){
  'use strict';

  angular
    .module('lima', [
      'lima.controller',
      'lima.routes',
      'lima.maps',
      'lima.config'
    ]);

    angular
      .module('lima.config', []);

    angular
      .module('lima.routes', ['ngRoute']);

    angular
      .module('lima.controller', ['pusher-angular', 'uiGmapgoogle-maps']);

    angular
      .module('lima')
      .run(run);

    run.$inject = ['$http'];

    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    };

})();
