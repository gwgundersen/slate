/* Generates all plots for report pages.
 */

window.plotExpenses = function(expensesData, perDayData) {

    Highcharts.setOptions({
        chart: {
            style: {
                fontFamily: 'Arial, sans-serif'
            }
        },
        colors: [
            '#D40000', // alcohol
            '#395200', // bills
            '#41a1ed', // clothing
            '#FFE11A', // entertainment
            '#0b4370', // food (in)
            '#FD7400', // food (out)
            '#7FB800', // household
            '#1689E5', // medical
            '#5c8500', // miscellaneous
            '#0f5f9f', // transportation (away)
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

    var data = [],
        breakoutData = [];
    $.each(perDayData, function(date, obj) {
        var d = date.split('-'),
            total = 0;
        $.each(obj, function(i, e) {
            total += e.cost;
        });

        // Subtract 1 because JavaScript counts months from 0...
        data.push([Date.UTC(d[0], d[1]-1, d[2]), total]);
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
        tooltip: {
            formatter: function() {

                function dayOfWeekAsString(dayIndex) {
                    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][dayIndex];
                }

                var idx = this.series.data.indexOf(this.point),
                    date = new Date(this.x),
                    day = dayOfWeekAsString(date.getDay()),
                    table = '<strong>' + day + '</strong><br>';

                // Don't show empty tooltip.
                if (!perDayData[idx].expenses.length) {
                    return false;
                }

                // Highcharts does not support tables. For a list of support
                // HTML elements:
                // http://api.highcharts.com/highcharts#tooltip
                $.each(perDayData[idx].expenses, function(i, e) {
                    table += '' +
                        '<span>$' + e.cost + ' - ' + e.comment + '</span><br>';
                });
                return table;
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
