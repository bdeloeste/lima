


// function map(stream, keyword, start_date, end_date){
//   return $http.post('/api/v1/map',{
//     if (end_date && start_date == null) {
//       stream = true;
//     }
//   }).then();
// };
//
// $("#search-form").dialog ({
//   buttons:{
//   "Search": function(){
//     return $http.post('/api/v1/map',{
//       success: function(data) {
//         var obj=data;
//         alert(JSON.stringify(obj));
//       }
//     })
//   }
// });
// }
  //
  // app.controller('searchCtrl', function($scope,$http){
  //   $http.get('data.json').success(function(data,status,headers,config){
  //     $scope.items = data.data;
  //   }).error(function(data,status,headers,config){
  //     console.log('No data found');
  //   });
  // });
  // app.filter('searchFor', function(){
  //   return function(arr, searchString){
  //     if(!searchString){
  //       return arr;
  //     }
  //     var result=[];
  //     searchString = searchString.toLowerCase();
  //     angular.forEach(arr, function(item){
  //       if(item.title.toLowerCase().indexOf(searchString)!==-1){
  //         result.push(item);
  //       }
  //     });
  //     return $http.post('/api/v1/accounts');
  //   };
  // });
// (function() {
//   'use strict';
//
//   angular
//     .module('lima.maps.controllers')
//     .controller('searchCtrl', searchCtrl);
//
//   searchCtrl.$inject = ['$scope', '$http', 'maps'];
//
//   function searchCtrl($scope, $http, maps) {
//     var vm = this;
//     vm.search = search;
//
//     function search() {
//       return $http.post('/api/v1/maps', {
//         keyword: vm.content,
//       });
//
//       maps.searching(vm.content).then(searchKeywordSuccessFn, searchKeywordErrorFn);
//
//       function searchKeywordSuccessFn(data, status, headers, config) {
//         console.error('Oops');
//       }
//
//       function searchKeywordErrorFn(data, status, headers, config) {
//         console.error('Oops Oops');
//       }
//     }
//
  //   activate();
  //
  //   function activate(stream, keyword, start_date, end_date) {
  //     var results = [];
  //     if (end_date && start_date == null) {
  //       stream = true;
  //       results.push(keyword);
  //     }
  //     else {
  //       stream = false;
  //     }
  //     maps.searching(vm.content).then(searchKeywordSuccessFn);
  //   }
  // }
// function search(stream, keyword, start_date, end_date) {
//   var results = [];
//   if (end_date && start_date == null) {
//     stream = true;
//     results.push(keyword);
//   }
//   return $http.post('/api/v1/map');
// };
