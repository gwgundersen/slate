window.plotExpenses = function(expensesData, perDayData) {

    Highcharts.setOptions({
        chart: {
            style: {
                fontFamily: 'Arial, sans-serif'
            }
        },
        colors: [
            '#E74C3C', // alcohol
            '#035D0E', // bills
            '#004358', // clothing
            '#FFE11A', // entertainment
            '#2C3E50', // food (in)
            '#FD7400', // food (out)
            '#BEDB39', // household
            '#1689E5', // medical
            '#1F8A70',  // miscellaneous
            '#3498DB', // transportation (away)
            '#2980B9'  // transportation (local)
        ]
    });

    plotExpensesPieChart(expensesData);
    plotExpensesByCategory(expensesData);
    plotExpensesTimeSeries(perDayData);
};

window.plotExpensesPieChart = function(expensesData) {

    var data = [];
    $.each(expensesData, function(i, obj) {
        data.push({
            name: obj.category,
            y: obj.subtotal
        });
    });

    // Build the chart
    $('#pie-chart-container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: '% expenses by category'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Subtotal',
            colorByPoint: true,
            data: data
        }]
    });
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
            text: '$ expenses by day'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Subtotal'
            },
            // Lowest allowed value on y-axis.
            floor: 0
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
            height: 350
        },
        colors: ['#1689E5'],
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
        plotOptions: {
            bar: {
                //height: 10,
                dataLabels: {
                    enabled: true
                }//,
                //pointWidth: 14
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