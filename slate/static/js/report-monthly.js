/* Generates all plots for report pages.
 */

window.plotExpenses = function(categorySubtotals, expenses) {

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

    plotExpensesPieChart(categorySubtotals);
    plotExpensesByCategory(categorySubtotals);
    plotExpensesTimeSeries(expenses);
};

window.plotExpensesPieChart = function(categorySubtotals) {

    var data = [];
    $.each(categorySubtotals, function(i, obj) {
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

window.plotExpensesByCategory = function(categorySubtotals) {

    var categories = [],
        series = [];

    $.each(categorySubtotals, function (i, obj) {
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

window.plotExpensesTimeSeries = function(days) {

    var data = [];
    $.each(days, function(dateStr, expenses) {
        console.log(dateStr);
        var total = 0;
        $.each(expenses, function(i, e) {
            total += e.cost;
        });

        var t = new Date(dateStr);
        var d = dateStr.split('-');
        var seconds = Date.UTC(d[0], d[1], d[2]);
        data.push([seconds, total]);
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

                debugger;
                var idx = this.series.data.indexOf(this.point),
                    d = new Date(this.key),
                    dayString = dayOfWeekAsString(d.getDay()),
                    table = '<strong>' + dayString + '</strong><br>';

                // Don't show empty tooltip.
                if (!expenses[this.key].length) {
                    return false;
                }

                // Highcharts does not support tables. For a list of support
                // HTML elements:
                // http://api.highcharts.com/highcharts#tooltip
                $.each(expenses[this.key], function(i, e) {
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
