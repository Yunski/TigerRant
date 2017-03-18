var ENTER_KEY = 13;

$(window).on("load", function() {
    AOS.init();
});

$(window).scroll(function() {
    if ($(document).scrollTop() > 50) {
        $("#navbar-home").addClass("shrink");
        //$(".navbar").addClass("fixed-top");
    } else {
        $("#navbar-home").removeClass("shrink");
        $("#navbar-home").css("-webkit-transition", "height 300ms ease-in-out");
        $("#navbar-home").css("-moz-transition", "height 300ms ease-in-out");
        $("#navbar-home").css("-o-transition", "height 300ms ease-in-out");
        $("#navbar-home").css("transition", "height 300ms ease-in-out");
        //$(".navbar").removeClass("fixed-top");
    }
});

$(document).ready(function() {
    $("#navbar-browse .search-button").click(function() {
        window.location.href = "/browse";
    });

    /* TEMPORARY LOGOUT TESTING - TODO: FIX THIS! */
    $("#nav-account").click(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/logout',
            type: 'post',
            success: function() {
                window.location.href = "/";
            }
        });
    });
    /* search logic */
    $(".search-text-field").bind("keypress", function(e) {
        if (e.keyCode == ENTER_KEY) {
            var searchText = $(".search-text-field").val();
            if (searchText == "") return;
            document.location.href = "/browse?search=" + searchText + "&page=1";
            //console.log(searchText);
            e.preventDefault();
            return false;
        }
    });

    $(".search-button").click(function() {
        var searchText = $(".search-text-field").val();
        if (searchText == "") return;
        document.location.href = "/browse?search=" + searchText + + "&page=1";
        //console.log(searchText);
    });

    /* pagination */
    $(".page-link").click(function(e) {
        e.preventDefault();
        page = $(this).text();
        newPageURL = window.location.href;
        baseURL = "";
        queryString = "";
        pageParam = "page=";
        if (newPageURL.indexOf("?") >= 0) {
            components = newPageURL.split("?");
            baseURL = components[0] + "?";
            queryString = components[1];
            if (queryString.indexOf("page") >= 0) {
                currentPage = queryString.split(pageParam)[1];
                if (page.toLowerCase() === "next") {
                    pageInt = parseInt(currentPage);
                    if (pageInt != NaN) {
                        page = (pageInt + 1).toString();
                    }
                } else if (page.toLowerCase() === "previous") {
                    pageInt = parseInt(currentPage);
                    if (pageInt != NaN) {
                        page = (pageInt - 1).toString();
                    }
                }
                queryString = queryString.split(pageParam)[0] + pageParam + page;
            }
        } else {
            /* TEMPORARY - first time on browse, load all courses */
            baseURL = newPageURL;
            console.log(page);
            if (page.toLowerCase() === "next") {
                queryString = "?page=2";
            } else {
                queryString = "?page=" + page;
            }
        }
        //console.log(baseURL + queryString);
        document.location.href = baseURL + queryString;
    });
});
