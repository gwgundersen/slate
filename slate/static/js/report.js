window.plotExpenses = function(expensesData, perDayData) {

    Highcharts.setOptions({
        chart: {
            style: {
                fontFamily: 'Arial, sans-serif'
            }
        }
    });

    plotExpensesByCategory(expensesData);
    plotExpensesTimeSeries(perDayData);
};

window.plotExpensesTimeSeries = function(perDayData) {

    var data = [];
    $.each(perDayData, function(i, obj) {
        var d = obj.date_time;
        // Subtract 1 because JavaScript counts months from 0...
        data.push([Date.UTC(d[0], d[1]-1, d[2]), obj.total]);
    });

    $('#time-series-container').highcharts({
        chart: {
            zoomType: 'x'
        },
        colors: ['#1689E5'],
        title: {
            text: 'Expenses by day'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Subtotal'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            type: 'area',
            name: 'Subtotal',
            data: data
        }]
    });
};

window.plotExpensesByCategory = function(expensesData) {

    var categories = [],
        series = [];

    $.each(expensesData, function (i, obj) {
        categories.push(obj.category);
        series.push(obj.subtotal);
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