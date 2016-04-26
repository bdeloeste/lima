(function () {
  'use strict';

  angular
    .module('lima.maps.services')
    .factory('Search', Search);

    Search.$inject = ['$location','$http'];

    function Search($location,$http) {

      // var Search = {};
      // Search.arrSearchResults = [];
      // Search.searchTerm = "";


      Search.submitSearch = function(keyword) {
        // $location.search('q', keyword);
        // Search.searchTerm = keyword;

        return $http.post('/api/v1/maps', $.param({
          stream: true,
          keywords: keyword
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            // 'X-Requested-With': 'XMLHttpRequest'
        }
        }).then(success, error);

        function success(data, status, headers, config) {
            console.log("i made it mom");
            Search.template = "/static/templates/map.html";
        }

        function error(data, status, headers, config) {
            console.log("i got arrested sorry");
        }
      }
      return Search;
    }

})();