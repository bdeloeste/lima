/**
 * Created by delo on 4/18/16.
 */
(function () {
  'use strict';

  angular
    .module('lima.maps.services')
    .factory('tweetData', tweetData);

    tweetData.$inject = ['$location','$http'];

    function tweetData($location, $http) {
      var dataList = [];
      var dataPoints = [];
      var total_lima= [0, 0, 0, 0], count = [0, 0, 0, 0], avg_lima = [8, 0, 0, 0];

      tweetData.getPoints = function() {
        // console.log(avg_lima);
        return avg_lima;
      }

      tweetData.getSentiment = function(data) {
        dataList.push(data);

        //iterates through list
        angular.forEach(dataList, function(value, key) {
          var loc = Math.floor(Math.random() * 4); //random number 0 - 3. 0 = SF, 1 = ATX etc..

          //adds sentiment to total_lima
          total_lima[loc] += value.sentiment;

          //count acts as length of total_lima
          count[loc] += 1;
          avg_lima[loc] = total_lima[loc]/count[loc];
          return avg_lima[loc];
        });
       };

      return tweetData
    }
})();