$(document).ready(function() {
    $("#logout-link").click(function() {
        $.ajax({
            url: "/logout",
            type: "POST",
            success: function(data) {
            }
        });
    });
});
