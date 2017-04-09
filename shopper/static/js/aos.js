$(window).on("load", function() {
    AOS.init();
    $(".resizing-search-option").html($('.search-options option:first').text());
    $(".search-options").width($(".resizing-search-select").width() + 4);
    $(".search-options").css("background-position-x", ($(".resizing-search-select").width() + 20).toString() + "px");
});
