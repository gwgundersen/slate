window.plot = function(data) {

    // We might want this in the future. For now, it really skews the plot.
    delete data['rent'];

    function transform(data) {
        var results = [];
        for (var i = 0; i < data.length; i++) {
            var obj = data[i];
            results.push([
                Date.UTC(obj.datetime[0], obj.datetime[1]-1, obj.datetime[2]),
                obj.cost
            ]);
        }
        return results;
    }

    var series = [];
    $.each(data, function(key, series_data) {
        series.push({
            name: key,
            data: transform(series_data[0]) 
        });
    });

    $('#container').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: 'All Expenses'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                month: '%e. %b',
                year: '%b'
            },
            title: {
                text: 'Date'
            }
        },
        yAxis: {
            title: {
                text: 'Snow depth (m)'
            },
            min: 0
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x:%e. %b}: ${point.y:.2f}'
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled: true
                }
            }
        }, 
        series: series
    });
};
