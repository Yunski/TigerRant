var rating = 0;

function detectStarHover() {
    if (rating == 0) {
        $(".initial-rating span").mouseover(function() {
            id = this.id.split("star")[1];
            for (var i = 1; i <= 5; i++) {
                if (i <= id) {
                    $("#star"+i).addClass("active");
                } else {
                    $("#star"+i).removeClass("active");
                }
            }
        });
        $(".initial-rating span").mouseleave(function() {
            for (var i = 1; i <= 5; i++) {
                $("#star"+i).removeClass("active");
            }
        });
    }
}

function selectStar() {
    $(".initial-rating span").click(function() {
        id = this.id.split("star")[1];
        rating = id * 1.0;
        for (var i = 1; i <= 5; i++) {
            if (i <= id) {
                $("#star"+i).addClass("active");
            } else {
                $("#star"+i).removeClass("active");
            }
        }
    });
}

function animateBars() {
    var mockRatings = [0, 15, 60, 5, 10];
    /* rating bar animation */
    $(".rating-bars .rating-bar-inner").each(function(index) {
        $(this).width(mockRatings[index] + '%');
    });
}

$(document).ready(function() {
    //detectStarHover();
    selectStar();
    animateBars();

    $("#sidebar-btn").click(function(e) {
        e.preventDefault();
        $("#course-page-content").toggleClass("toggled");
    });

    $("textarea").each(function () {
    }).on("input", function () {
      this.style.height = "auto";
      this.style.height = (this.scrollHeight) + "px";
    });

    $("#more-descriptions-button").click(function () {
        if ($("#more-button-container a").hasClass("collapsed")) {
            $("#more-button-container a").text("Show Less");
        } else {
            $("#more-button-container a").text("Show More");
        }
    });

    $("#review-cancel-button").click(function() {
        rating = 0;
    });

    $("#review-post-button").click(function() {
        var text = $("#review-text").val();
        if (text == "" || rating == 0) return;
        sem_code = $("#term").attr("data-term");
        console.log(sem_code);
        console.log(rating);
        console.log(text);
        c_id = parseInt(window.location.href.split("id=")[1]);
        $.ajax({
            url: "/api/reviews/" + c_id,
            type: "POST",
            data: {sem_code: sem_code, rating: rating, text: text},
            success: function(data) {
                console.log("Response " + JSON.stringify(data));
                location.reload();
            }
        });
    });

    $("#description-post-button").click(function() {
        var text = $("#description-text").val();
        if (text == "") return;
        c_id = parseInt(window.location.href.split("id=")[1]);
        $.ajax({
            url: "/api/descriptions/" + c_id,
            type: "POST",
            data: {text: text},
            success: function(data) {
                console.log("Response " + JSON.stringify(data));
                location.reload();
            }
        });
    });
});

$.fn.extend({
    animateCss: function (animationName) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        this.addClass('animated ' + animationName).one(animationEnd, function() {
            $(this).removeClass('animated ' + animationName);
        });
    }
});

function scrollToReviewsTop() {
    console.log($("#course-page-content").offset().top);
    $("#course-page-content").animate({
        scrollTop: 520
    }, 500);
}
