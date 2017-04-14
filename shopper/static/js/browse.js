var options = {};
options[0] = "dept";
options[1] = "rating";
var selected = {};
selected["dept"] = 0;
selected["rating"] = 1;

$(window).on("load", function() {
    var selectedValue = window.location.href.split("order=")[1].split("&")[0];
    var value = selected[selectedValue];
    if (value) {
        $(".sort-options").val(value);
    }
});

$(document).ready(function() {
    /* sort */
    $(".sort-options").change(function() {
        var selected = $(".sort-options").val();
        document.location.href = window.location.href.split("&order")[0] + "&order=" + options[selected];
    });
    /* pagination */
    $(".course-link").click(function(e) {
        e.preventDefault();
        page = $(this).text();
        newPageURL = window.location.href;
        baseURL = "";
        queryString = "";
        pageParam = "page=";
        orderParam = "order=";
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
                order = queryString.split(orderParam)[1];
                queryString = queryString.split(pageParam)[0] + pageParam + page + "&" + orderParam + order;
            }
        }
        //console.log(baseURL + queryString);
        document.location.href = baseURL + queryString;
    });
});
