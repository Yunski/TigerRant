var ENTER_KEY = 13;

$(window).on("load", function() {
    AOS.init();
    $(".resizing-search-option").html($('.search-options option:first').text());
    $(".search-options").width($(".resizing-search-select").width() + 4);
    $(".search-options").css("background-position-x", ($(".resizing-search-select").width() + 20).toString() + "px");
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

    $('.search-options').change(function() {
        $(".resizing-search-option").html($('.search-options option:selected').text());
        $(this).width($(".resizing-search-select").width() + 4);
        $(this).css("background-position-x", ($(".resizing-search-select").width() + 20).toString() + "px");
    });

    /*
    $('.sort-options').change(function(){
        $(".resizing-sort-option").html($('.sort-options option:selected').text());
        $(this).width($(".resizing-sort-select").width());
    });*/

    $("#logout-link").click(function(e) {
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
            e.preventDefault();
            return false;
        }
    });

    $(".search-button").click(function(e) {
        e.preventDefault();
        var searchText = $(".search-text-field").val();
        if (searchText == "") return;
        document.location.href = "/browse?search=" + searchText + "&page=1";
    });

    /* pagination */
    $(".course-link").click(function(e) {
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
                pageInt = parseInt(currentPage);
                if (isNaN(pageInt)) {
                    pageInt = 1;
                }
                if (page.toLowerCase() === "next") {
                    page = (pageInt + 1).toString();
                } else if (page.toLowerCase() === "previous") {
                    page = (pageInt - 1).toString();
                }
                queryString = queryString.split(pageParam)[0] + pageParam + page;
            }
        } else {
            /* TEMPORARY - first time on browse, load all courses */
            baseURL = newPageURL;
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

function scrollToReviewsTop() {
    $('html, body').animate({
        scrollTop: $(".terms").offset().top
    }, 500);
}
