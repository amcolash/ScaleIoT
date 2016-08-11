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
        	type: 'week',
        	count: 1,
        	text: '1w'
        }, {
          type: 'week',
        	count: 2,
        	text: '2w'
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
        selected: 5 // choose the 2 weeks previous by default
      },
      series: [{}],
      title: {
        text: 'Recent Weights'
      },
      tooltip: {
        xDateFormat: '%A, %B %d, %l:%M%p',
        valueDecimals: 1,
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
    var high = -999;
    var low = 999;
    var averageWeight = 0;
    var totalWeights = 0;

    var date = new Date();
    var current = date.getTime();
    var previousMonth = current - (1000 * 60 * 60 * 24 * 30);

    $.each(data, function(key, value) {
      value = parseFloat(value);
      series.push([parseInt(key), value]);

      // Set last weight based on last time (handles incorrectly sorted lists)
      if (parseInt(key) > lastTime) {
        lastTime = parseInt(key);
        lastWeight = value;
      }

      // Only keep track of the past month of averages
      if (parseInt(key) >= previousMonth) {
        if (value < low) {
          low = value;
        }

        if (value > high) {
          high = value;
        }

        averageWeight += value;
        totalWeights ++;
      }
    });

    if (lastWeight > 0) {
      $('#lastWeight').text(lastWeight.toFixed(1) + ' lbs');
    } else {
      $('#lastWeight').text('?');
    }

    if (averageWeight > 0 && totalWeights > 0) {
      averageWeight = averageWeight / totalWeights;
      $('#averageWeight').text(averageWeight.toFixed(1) + ' lbs');
    } else {
      $('averageWeight').text('?');
    }

    if (low < 999) {
      $('#lowWeight').text(low.toFixed(1) + ' lbs');
    } else {
      $('lowWeight').text('?');
    }

    if (high > -999) {
      $('#highWeight').text(high.toFixed(1) + ' lbs');
    } else {
      $('highWeight').text('?');
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
    options.series[0].color = '#99ecf1';
    options.series[0].name = 'Weight';

    // Add trendline
    options.series[0].regression = true;
    options.series[0].regressionSettings = {
        type: 'polynomial',
        color:  '#00A6FF',
        name: 'Average Weight',
        lineWidth: 4,
        tooltip: {
          valueDecimals: 1,
          valueSuffix: ' lbs'
        }
    };

    var chart = new Highcharts.StockChart(options);
  });

});
