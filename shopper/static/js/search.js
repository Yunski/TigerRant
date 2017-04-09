var ENTER_KEY = 13;

$(document).ready(function() {
    $(".search-text-field").mouseover(function() {
        $(".search-text-field").css("border-top", "1px solid #ee7f2d");
        $(".search-text-field").css("border-bottom", "1px solid #ee7f2d");
        $(".input-label").css("border-top", "1px solid #ee7f2d");
        $(".input-label").css("border-left", "1px solid #ee7f2d");
        $(".input-label").css("border-bottom", "1px solid #ee7f2d");
        $(".search-button").css("border", "1px solid #ee7f2d");
    });
    $(".search-text-field").mouseleave(function() {
        $(".search-text-field").css("border-top", "1px solid white");
        $(".search-text-field").css("border-bottom", "1px solid white");
        $(".input-label").css("border-top", "1px solid white");
        $(".input-label").css("border-left", "1px solid white");
        $(".input-label").css("border-bottom", "1px solid white");
        $(".search-button").css("border", "1px solid white");
    });

    /* search logic */
    $(".search-text-field").bind("keypress", function(e) {
        if (e.keyCode == ENTER_KEY) {
            var searchText = $(".search-text-field").val();
            if (searchText == "") return;
            document.location.href = "/browse?search=" + searchText + "&page=1&order=dept";
            e.preventDefault();
            return false;
        }
    });

    $(".search-button").click(function(e) {
        e.preventDefault();
        var searchText = $(".search-text-field").val();
        if (searchText == "") return;
        document.location.href = "/browse?search=" + searchText + "&page=1&order=dept";
    });
});
