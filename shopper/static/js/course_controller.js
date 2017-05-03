(function () {

    'use strict';

    angular.module('TigerShop', [])
    .config( [ '$locationProvider', '$interpolateProvider', function( $locationProvider, $interpolateProvider ) {
       // In order to get the query string from the
       // $location object, it must be in HTML5 mode.
       $locationProvider.html5Mode(true);
       $interpolateProvider.startSymbol('{a');
       $interpolateProvider.endSymbol('a}');
    }])
    .controller('TigerShopController', ['$scope', '$log', '$http', '$location', '$window',
        function($scope, $log, $http, $location, $window, $document) {
            var id = -1;
            var search = "";
            var page = "";
            var order = "";
            var maxPerPage = 20;

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
                          $scope.approvedDescriptions = [];
                          $scope.purgatoryDescriptions = [];
                          for (var i in descriptions) {
                              var description = descriptions[i];
                              if (description.upvotes < 10) {
                                  $scope.purgatoryDescriptions.push(description);
                              } else {
                                  $scope.approvedDescriptions.push(description);
                              }
                          }
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
            $scope.getHotRants = function() {
                $http.get('/api/rants/' + id + '/true').
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
                            var terms = []
                            $scope.terms = reviews;
                            for (var term in reviews) {
                                terms.push(term);
                                $scope.terms[term]['average_rating'] = $scope.terms[term]['average_rating'].toFixed(1).toString();
                            }
                            if (terms.length > 0) {
                                for (var i = terms.length-1; i >= 0; i--) {
                                    var length = $scope.terms[terms[i]]['reviews'].length;
                                    if (length > 0) {
                                        $scope.selectedTerm = terms[i];
                                        break;
                                    }
                                }
                                if (!$scope.selectedTerm) $scope.selectedTerm = terms[0];
                            }
                            if ($scope.terms[$scope.selectedTerm]['reviews'].length > 0) {
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
            $scope.updateDescription = function($index, vote, isApproved) {
                var data = $.param({
                    vote: vote
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                var description = isApproved ? $scope.approvedDescriptions[$index] : $scope.purgatoryDescriptions[$index];
                var descriptionId = description.id;
                $http.put('/api/descriptions/' + descriptionId, data, config).
                      success(function(response, status) {
                          if (status == 201) {
                              if (isApproved) {
                                  description.upvotes = response.upvotes;
                              } else {
                                  description.upvotes = response.upvotes;
                              }
                          }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            }
            $scope.updateRant = function($index, vote) {
                var data = $.param({
                    vote: vote
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                var rant = $scope.rants[$index];
                var rantId = rant.id;
                $http.put('/api/rants/' + rantId, data, config).
                      success(function(response, status) {
                          if (status == 201) {
                              rant.upvotes = response.upvotes;
                          }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            }
            $scope.updateReply = function($rantIndex, $replyIndex, vote) {
                var data = $.param({
                    vote: vote
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                var reply = $scope.rants[$rantIndex].replies[$replyIndex];
                var replyId = reply.id;
                $http.put('/api/replies/' + replyId, data, config).
                      success(function(response, status) {
                          if (status == 201) {
                              reply.upvotes = response.upvotes;
                          }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            }
            $scope.updateReview = function($index, score) {
                var data = $.param({
                    score: score
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                var review = $scope.reviews[$index];
                var reviewId = review.id;
                $http.put('/api/reviews/' + reviewId, data, config).
                      success(function(response, status) {
                          if (status == 201) {
                              review.score = response.score;
                          }
                      }).
                      error(function(error) {
                          $log.log(error);
                      });
            }
            $scope.postReply = function($index) {
                var rant = $scope.rants[$index];
                var rantId = rant.id;
                var text = $("#your-reply-" + rantId + " textarea").val();
                if (text == "") return;
                var data = $.param({
                    text: text
                });
                var config = {
                    headers : {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
                    }
                }
                $http.post('/api/replies/' + rantId, data, config).
                      success(function(reply, status) {
                          if (status == 201) {
                              rant.replies.push(reply);
                          }
                          $("#your-reply-" + rantId).collapse("hide");
                          $("#your-reply-" + rantId + " textarea").val("");
                      }).
                      error(function(error) {
                          $log.log(error);
                          $("#your-reply-" + rantId).collapse("hide");
                      });
            }
            $scope.getDescriptions();
            $scope.getRants();
            $scope.getReviews();
        }
    ]);
}());
