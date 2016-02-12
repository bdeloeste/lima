(function(angular){
  'use strict';
  angular
    .module('lima', []);
    .controller('searchCtrl', ['$scope', function($scope){
      $scope.keyword = "Testing";

      $scope.display = function() {
        $scope.result = $scope.keyword + "1, 2, 3";
      };
    }]);
});
