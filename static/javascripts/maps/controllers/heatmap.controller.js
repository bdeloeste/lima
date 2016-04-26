/**
 * Created by delo on 4/18/16.
 */
(function () {
  'use strict';

  angular
    .module('lima.maps.controllers')
    .controller('LayerHeatmapCtrl', LayerHeatmapCtrl);

  LayerHeatmapCtrl.$inject = ['$scope', '$interval', '$timeout', 'tweetData', 'Search', 'uiGmapGoogleMapApi', '$pusher'];

  function LayerHeatmapCtrl($scope, $interval, $timeout, tweetData, Search, uiGmapGoogleMapApi, $pusher) {
    var vm = this;
    var client = new Pusher('b87e84a0194862d39bdd');
    var pusher = $pusher(client);
    var data_queue = new Queue();
    var ids = 1;
    var totalSentiment = 0;
    $scope.title = "Location Inference Data";
    $scope.tweetsCollected = 0;
    $scope.averageSentiment = 0;
    $scope.circles = [];
    $scope.randomMarkers = [];
    $scope.window = {
        'coords': {
            latitude: 20.8859,
            longitude: -130.4629
        }
    };
    $scope.windowOptions = {
        visible: true
    };
    pusher.subscribe('lima');
    pusher.bind('tweet_stream',
      function(data) {
        // console.log(data.data.text);
        // console.log(data.data.sentiment);
        var locData = {
            'text': data.data.text,
            'sentiment': data.data.sentiment,
            'coordinates': data.data.coordinates.coordinates
        };
        console.log(locData);
        data_queue.enqueue(locData);
        $scope.tweetsCollected += 1;
        totalSentiment += data.data.sentiment;
        $scope.averageSentiment = (totalSentiment / $scope.tweetsCollected).toFixed(4);
        // console.log(data_queue);
      });      
    uiGmapGoogleMapApi.then(function(maps){
      var local_layer, heatLayer;
      $interval(function() {
        MockHeatLayer();
      }, 100);

      $scope.map = {
        center: {
          latitude: 37.09024,
          longitude: -95.712891
        },
        zoom: 4
      };
    });

    function MockHeatLayer() {
      // console.log('ah');
      // var pointArray = tweetData.getPoints();
      // testmarkers();
      // testCircles();
      if (!(data_queue.isEmpty())) {
          console.log('Setting circles');
          setCircles(data_queue);
      }
      // setCircles(pointArray[0], pointArray[1], pointArray[2], pointArray[3]);
    }

    function getColor(sent) {
      var hue = 60 * (sent + 1);
      return 'hsl(' + hue + ', 100%, 50%)';
    }

    function testmarkers() {
      $scope.randomMarkers = [
            { //San Francisco
              id: 1,
              latitude: 37.7833,
              longitude: -122.4167
            },
            { //Chicago
              id: 2,
              latitude: 41.8369,
              longitude: -87.6847
            },
            { //NYC
              id: 3,
              latitude: 40.1727,
              longitude: -74.0059
            },
            { //Austin
                id: 4,
                latitude: 30.25,
                longitude: -97.75
            },
            { //Austin
                id: 5,
                latitude: 30.26,
                longitude: -97.75
            },
            { //Austin
                id: 6,
                latitude: 30.27,
                longitude: -97.75
            },
            { //Austin
                id: 7,
                latitude: 30.26,
                longitude: -97.8
            }
          ];
    }

    function testCircles() {
        for (var i = 0; i < 3; i++) {
            var circleObject = {
                id: ids,
                center: {
                    latitude: 37.7833,
                    longitude: -122.4167
                },
                radius: 50000,
                stroke: {
                    color: getColor(1),
                    weight: 2,
                    opacity: 1
                },
                fill: {
                    color: getColor(0.5),
                    opacity: 0.5
                }
            };
            $scope.circles.push(circleObject);
            ids += 1;
        }
    }

    function setCircles(data) {
        for (var i = 0; i < data.getLength(); i++) {
            var dataInfo = data.dequeue();
            console.log(dataInfo);
            var circleObject = {
                id: ids,
                center: {
                    latitude: dataInfo['coordinates'][1],
                    longitude: dataInfo['coordinates'][0]
                },
                radius: 50000,
                stroke: {
                    color: getColor(dataInfo['sentiment']),
                    weight: 2,
                    opacity: 1
                },
                fill: {
                    color: getColor(dataInfo['sentiment']),
                    opacity: 0.5
                }
            };
            var markerObject = {
                id: ids,
                latitude: dataInfo['coordinates'][1],
                longitude: dataInfo['coordinates'][0]
            };
            $scope.circles.push(circleObject);
            $scope.randomMarkers.push(markerObject);
            ids += 1;
        }

    }
  }
})();