(function () {

    'use strict';

    angular.module('TigerShop', [])
    .config( [ '$locationProvider', function( $locationProvider ) {
       // In order to get the query string from the
       // $location object, it must be in HTML5 mode.
       $locationProvider.html5Mode(true);
    }])
    .controller('TigerShopController', ['$scope', '$log', '$http', '$location',
        function($scope, $log, $http, $location) {
            var id = -1;
            var search = "";
            var page = "";
            var order = "";
            var maxPerPage = 20;
            $scope.tab = 0;

            $scope.setTab = function (newTab) {
              $scope.tab = newTab;
            };

            $scope.isSetOn = function (newTab) {
              return $scope.tab === newTab;
            };

            if ( $location.search().hasOwnProperty('id')) {
                id = $location.search().id;
            }
            if ( $location.search().hasOwnProperty('search')) {
                search = $location.search().search;
            }
            if ( $location.search().hasOwnProperty('page')) {
                page = $location.search().page;
            }
            if ( $location.search().hasOwnProperty('order')) {
                order = $location.search().order;
            }
            $scope.returnURL = "/browse?search=" + search + "&page=" + page + "&order=" + order;
            $scope.getDescriptions = function() {
                $http.get('/api/descriptions/' + id).
                      success(function(descriptions) {
                          $scope.descriptions = descriptions;
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            };
            $scope.getRants = function() {
                $http.get('/api/rants/' + id).
                      success(function(rants) {
                          $scope.rants = rants;
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            };
            $scope.getReviews = function() {
                $http.get('/api/reviews/' + id).
                      success(function(reviews) {
                            var termInts = []
                            $scope.terms = {}
                            for (var term in reviews) {
                                $scope.terms[term] = {};
                                $scope.terms[term]['term_string'] = reviews[term]['term_string'];
                                termInts.push(parseInt(term));
                                var reviewList = reviews[term]['reviews'];
                                var total = 0;
                                for (var i in reviewList) {
                                    total += reviewList[i].overall_rating;
                                }
                                var average = (Math.round( total / reviewList.length * 10 ) / 10).toFixed(1);
                                $scope.terms[term]['average_rating'] = average.toString();
                                $scope.terms[term]['reviews'] = reviewList;
                            }
                            if (termInts.length > 0) {
                                $scope.selectedTerm = Math.max(...termInts).toString();
                            } else {
                                $scope.selectedTerm = "";
                            }
                            if ($scope.selectedTerm.length > 0) {
                                var currentPage = 1;
                                var totalReviews = $scope.terms[$scope.selectedTerm]['reviews'].length;
                                var start = 0;
                                var end = totalReviews < currentPage * maxPerPage ? totalReviews : currentPage * maxPerPage;
                                var pages = (totalReviews % maxPerPage) > 0 ? Math.floor(totalReviews / maxPerPage) + 1 : Math.floor(totalReviews / maxPerPage);
                                var pageLinks = [];
                                for (var i = 0; i < pages; i++) {
                                    if (i == currentPage-1) {
                                        pageLinks[i] = true;
                                    } else {
                                        pageLinks[i] = false;
                                    }
                                }
                                $scope.reviews = $scope.terms[$scope.selectedTerm]['reviews'].slice(start, end);
                                $scope.currentPage = currentPage;
                                $scope.pages = pages;
                                $scope.pageLinks = pageLinks;
                            }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            };
            $scope.getCourseData = function(term) {
                //$log.log(key);
                $scope.selectedTerm = term;
                var start = 0;
                var totalReviews = $scope.terms[$scope.selectedTerm]['reviews'].length;
                var currentPage = 1;
                var end = totalReviews < currentPage * maxPerPage ? totalReviews : currentPage * maxPerPage;
                var pages = (totalReviews % maxPerPage) > 0 ? Math.floor(totalReviews / maxPerPage) + 1 : Math.floor(totalReviews / maxPerPage);
                var pageLinks = [];
                for (var i = 0; i < pages; i++) {
                    if (i == 0) {
                        pageLinks[i] = true;
                    } else {
                        pageLinks[i] = false;
                    }
                }
                $scope.reviews = $scope.terms[$scope.selectedTerm]['reviews'].slice(start, end);
                $scope.pages = pages;
                $scope.pageLinks = pageLinks;
                $scope.currentPage = currentPage;
            };
            $scope.getReviewsForPage = function(event) {
                var currentPage = event.currentTarget.text;
                if (currentPage.toLowerCase() === "previous") {
                    $scope.currentPage -= 1;
                } else if (currentPage.toLowerCase() === "next") {
                    $scope.currentPage += 1;
                } else {
                    $scope.currentPage = parseInt(currentPage);
                }
                currentPage = $scope.currentPage;
                var start = (currentPage-1) * maxPerPage;
                var totalReviews = $scope.terms[$scope.selectedTerm]['reviews'].length;
                var end = totalReviews < currentPage * maxPerPage ? totalReviews : currentPage * maxPerPage;
                var pageLinks = [];
                for (var i = 0; i < $scope.pages; i++) {
                    if (i == currentPage-1) {
                        pageLinks[i] = true;
                    } else {
                        pageLinks[i] = false;
                    }
                }
                $scope.reviews = $scope.terms[$scope.selectedTerm]['reviews'].slice(start, end);
                $scope.pageLinks = pageLinks;
            };
            $scope.updateDescription = function(descriptionId, vote) {
                var data = $.param({
                    vote: vote
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                $http.put('/api/descriptions/' + id + '/' + descriptionId, data, config).
                      success(function(response, status) {
                          if (status == 201) {
                              $scope.getDescriptions();
                          }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            }
            $scope.updateRant = function(rantId, vote) {
                var data = $.param({
                    vote: vote
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                $http.put('/api/rants/' + id + "/" + rantId, data, config).
                      success(function(response, status) {
                          if (status == 201) {
                              $scope.getRants();
                          }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            }
            $scope.updateReview = function(reviewId, score) {
                var data = $.param({
                    score: score
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                $http.put('/api/reviews/' + id + '/' + reviewId, data, config).
                      success(function(response, status) {
                          if (status == 201) {
                              $scope.getReviews();
                          }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            }
            $scope.getDescriptions();
            $scope.getRants();
            $scope.getReviews();
        }
    ]);
}());
