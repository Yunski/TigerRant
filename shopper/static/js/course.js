function detectStarHover() {
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

function selectStar() {
    $(".initial-rating span").click(function() {
        $(".initial-rating").hide();
        $(".rating-bars").show();
        var mockRatings = [0, 15, 60, 5, 10];
        /* rating bar animation */
        $(".rating-bars .rating-bar-inner").each(function(index) {
            $(this).width(mockRatings[index] + '%');
        });
    });
}

$(document).ready(function() {
    detectStarHover();
    selectStar();

    $("#sidebar-btn").click(function(e) {
        e.preventDefault();
        $("#course-page-content").toggleClass("toggled");
    });

    $("#write-review-button").click(function() {
        console.log($(".reviews").offset().top);
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
        scrollTop: 560
    }, 500);
}
