$(document).ready(function() {
  var options = {
      chart: {
        renderTo: 'chart',
        type: 'spline'
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        series: {
          lineWidth: 4
        }
      },
      rangeSelector: {
        buttons: [{
          type: 'day',
          count: 3,
          text: '3d'
        }, {
        	type: 'week',
        	count: 1,
        	text: '1w'
        }, {
        	type: 'month',
        	count: 1,
        	text: '1m'
        }, {
        	type: 'month',
        	count: 3,
        	text: '3m'
        }, {
        	type: 'month',
        	count: 6,
        	text: '6m'
        }, {
        	type: 'all',
        	text: 'All'
        }],
        selected: 1 // choose 1 week previous
      },
      series: [{}],
      title: {
        text: 'Recent Weights'
      },
      tooltip: {
        xDateFormat: '%A, %B %d, %l:%M%p',
        valueSuffix: ' lbs',
      },
      xAxis: {
        type: 'datetime',
        title: {
          text: 'Date'
        }
      },
      yAxis: {
        offset: 24
      }
  };

  Highcharts.setOptions({
    global: {
      useUTC: false
    }
  });

  // Don't cache the json :)
  $.ajaxSetup({
    cache:false
  });

  $.getJSON('data.json', function(data) {
    var series = [];

    // Store some stats while parsing through
    var lastTime = 0;
    var lastWeight = 0;
    $.each(data, function(key, value) {
      value = parseFloat(value.toFixed(1));
      series.push([parseInt(key), value]);

      // Set last weight based on last time (handles incorrectly sorted lists)
      if (parseInt(key) > lastTime) {
        lastTime = parseInt(key);
        lastWeight = value;
      }
    });

    if (lastWeight > 0) {
      $('#lastWeight').text(lastWeight + ' lbs');
    } else {
      $('#lastWeight').text('Unknown');
    }

    // sort the dates because it doesn't seem like Python is doing it for us :/
    series.sort(function(a,b){
        if(a == b)
            return 0;
        if(a < b)
            return -1;
        if(a > b)
            return 1;
    });

    options.series[0].data = series;
    options.series[0].color = '#00a6ff';
    options.series[0].name = 'Weight';
    var chart = new Highcharts.StockChart(options);
  });

});
