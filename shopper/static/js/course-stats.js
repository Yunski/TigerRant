function detectStarHover() {
    $(".initial-rating span").bind('mouseover mouseleave click', function(event) {
        if (event.type == 'click') {
            activeItem = this;
        }
        else if (event.type == 'mouseover') {
            id = this.id.split("star")[1];
            for (var i = 1; i <= 5; i++) {
                if (i <= id) {
                    $("#star"+i).addClass("active");
                } else {
                    $("#star"+i).removeClass("active");
                }
            }
        }
        else if (event.type == 'mouseleave') {
          if (typeof activeItem != 'undefined') {
              if (activeItem != this) {
                  for (var i = 1; i <= 5; i++) {
                    $("#star"+i).removeClass("active");
                  }
                  activeItem = 'undefined'
              }
          }
        }
    });
}

function animateRatingBars() {
    var mockRatings = [0, 15, 60, 5, 10];
    /* rating bar animation */
    $(".rating-bars .rating-bar-inner").each(function(index) {
        $(this).width(mockRatings[index] + '%');
    });
}

$(document).ready(function() {
    detectStarHover();
    animateRatingBars();

    /*
    // Load the Visualization API and the corechart package.
    google.charts.load('current', {'packages':['corechart']});

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawChart);

    $("path").animate()
    /*
    $('.ai-response').fadeIn()
      .animate({top: 100}, 700);*/
});

function loadChart() {
  var data = [];
  $("#term-tab").click(function() {
      console.log(1);
      data = [
          ['Spring13-14',  2.89, 2.89],
          ['Spring14-15',  2.81, 2.82],
          ['Spring15-16',  3.00, 3.00]
      ];
      $(".comparison-options li:nth-of-type(1)").addClass('active');
      $(".comparison-options li:nth-of-type(2)").removeClass('active');
      drawChart(data);
  });
  $("#prof-tab").click(function() {
      console.log(2);
      data = [
          ['Spring13-14',  4.23, 4.23],
          ['Spring14-15',  1.83, 1.83],
          ['Spring15-16',  3.00, 3.00]
      ];
      $(".comparison-options li:nth-of-type(1)").removeClass('active');
      $(".comparison-options li:nth-of-type(2)").addClass('active');
      drawChart(data);
  });
}

function drawChart(dataTable) {
  var data = new google.visualization.DataTable();
    data.addColumn('string', 'Term');
    data.addColumn('number', 'Rating');
    data.addColumn({type:'number', role:'annotation'});
    data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});

    var dataTable = [
        ['Spring13-14',  2.89, 2.89, toolTipContent('Vanderbefwfwfefeefi', 2.89)],
        ['Spring14-15',  2.81, 2.81, toolTipContent('Vanderbei', 2.81)],
        ['Spring15-16',  3.00, 3.00, toolTipContent('Vanderbei', 3.00)]
    ];
    data.addRows(dataTable);

    var options = {
        theme: 'material',
        chartArea:{ top: '30', width:"90%", height:"80%" },
        legend: { position: "none" },
        colors: ['#e87722'],
        hAxis: {
          textStyle: {
              fontName: 'Futura-Light',
              fontSize: 14,
              // The color of the text.
              color: '#e87722',
          }
        },
        vAxis: {
            viewWindowMode:'explicit',
            viewWindow: {
                max: 5,
                min: 0
            }
        },
        annotations: {
            stemColor : 'none',
            textStyle: {
                fontName: 'Futura-Light',
                fontSize: 12,
                // The color of the text.
                color: '#e87722',
            }
        },
        tooltip: {
            isHtml: true,
        },
        pointSize: 8,
        animation:{
            startup:true,
            duration: 1000,
            easing: 'out'
        },
    };
    var formatter = new google.visualization.NumberFormat({fractionDigits:2});
    formatter.format(data, 2);

    var chart = new google.visualization.LineChart(document.getElementById('chart'));

    chart.draw(data, options);
}

function toolTipContent(professor, rating) {
  return '<div style="padding:5px 5px 5px 5px;font-family:"Futura-Light";text-align:center;">' +
      '<div style="display:inline-block;width: 90%;height:20px;"><b>' + professor + '</b></div>' +
      '<div style="display:inline-block;height:20px;">Rating: ' + rating.toFixed(2) + '</div>' + '</div>';
}
