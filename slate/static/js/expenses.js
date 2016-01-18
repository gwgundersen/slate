window.plotExpenses = function(rawData) {

    var categories = $.map(rawData, function (val, key) {
        return key;
    });
    var series = $.map(rawData, function (val, key) {
        return val;
    });

    Highcharts.setOptions({
        chart: {
            style: {
                fontFamily: 'Arial, sans-serif'
            }
        }
    });

    $('#bar-chart-container').highcharts({
        chart: {
            type: 'bar',
            height: 270
        },
        title: {
            text: ''
        },
        xAxis: {
            categories: categories,
            title: {
                text: ''
            },
            labels: {
                style: {
                    fontSize: '13px'
                }
            }
        },
        yAxis: {
            min: 0,
            labels: {
                overflow: 'justify',
                style: {
                    fontSize: '13px'
                }
            },
            title: {
                text: ''
            }
        },
        tooltip: {
            enabled: false
        },
        colors: ['#1689E5'],
        plotOptions: {
            bar: {
                //height: 10,
                dataLabels: {
                    enabled: true
                },
                pointWidth: 14
            },
            series: {
                pointPadding: 0,
                groupPadding: 0
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Expenses',
            data: series
        }]
    });
};