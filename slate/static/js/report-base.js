/* Generates plots that show up on all report pages.
 */

window.plotExpenses = function(categorySubtotals, expenses) {

    var colors = [
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
    ];

    Highcharts.setOptions({
        chart: {
            style: {
                fontFamily: 'Arial, sans-serif'
            }
        },
        credits: {
            enabled: false
        },
        colors: colors
    });

    plotExpensesPieChart(categorySubtotals);
    plotExpensesByCategory(categorySubtotals);
    plotExpensesTimeSeries(expenses);
    try {
        plotCategorySubtotalsPerMonth(expenses, categorySubtotals);
        plotCategorySparklines(expenses, categorySubtotals);
    } catch(e) {
        // Not on yearly report page.
    }
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
            type: 'bar'
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
                dataLabels: {
                    enabled: true
                }
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
        var total = 0;
        $.each(expenses, function(i, e) {
            total += e.cost;
        });
        var d = dateStr.split('-'),
            seconds = Date.UTC(d[0], d[1]-1, d[2]);
        data.push([seconds, total]);
    });

    $('#time-series-container').highcharts({
        chart: {
            zoomType: 'x'
        },
        colors: ['#1689E5'],
        title: {
            text: 'Expenses'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Daily subtotal'
            },
            // Lowest allowed value on y-axis.
            floor: 0
        },
        tooltip: {
            formatter: function() {

                function dayOfWeekAsString(dayIndex) {
                    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][dayIndex];
                }

                var d = new Date(this.key),
                    // Highcharts wants a UTC date in seconds. This converts it
                    // back to a Python datetime, e.g. 2017-01-01
                    key = d.toISOString().substr(0, 10),
                    dayString = dayOfWeekAsString(d.getDay()),
                    table = '<strong>' + dayString + '</strong><br>';

                // Don't show empty tooltip.
                if (!days[key].length) {
                    return false;
                }

                // Highcharts does not support tables. For a list of support
                // HTML elements:
                // http://api.highcharts.com/highcharts#tooltip
                $.each(days[key], function(i, e) {
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

window.plotCategorySparklines = function (days, categorySubtotals) {
    var $parent = $('#category-sparklines');
    $.each(categorySubtotals, function (i, obj) {
        createSparkline(i, obj.category.toLowerCase());
    });

    function dataForCategory(category) {
        var data = [],
            monthToData = {};
        $.each(days, function(dateStr, expenses) {
            var d = dateStr.split('-'),
                month = d[1]- 1,
                total = 0;
            if (typeof monthToData[month] === 'undefined') {
                monthToData[month] = 0;
            }
            $.each(expenses, function(j, e) {
                if (e.category === category) {
                    monthToData[month] += parseFloat(e.cost);
                }
            });
        });

        $.each(monthToData, function(month, total) {
            data[month] = total;
        });

        return data;
    }

    function createSparkline(i, category) {
        var id = 'cat-sparkline-' + i,
            data = dataForCategory(category);

        $parent.append('' +
            '<div class="sparkline-container">' +
                '<div class="sparkline-border">' +
                    '<div id="' + id + '" class="sparkline"></div>' +
                '</div>' +
            '</div>'
        );
        $parent.find('#' + id).highcharts({
            chart: {
                type: 'area'
            },
            colors: ['#1689E5'],
            title: {
                text: category
            },
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: 'Monthly $'
                }
            },
            legend: {
                enabled: false
            },
            tooltip: {
                enabled: false
            },
            plotOptions: {
                series: {
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    marker: {
                        enabled:false,
                        radius: 0,
                        states: {
                            hover: {
                                radius: 2
                            }
                        }
                    }
                }
            },
            series: [{
                type: 'area',
                data: data
            }]
        });
    }
};

window.plotCategorySubtotalsPerMonth = function (days, categorySubtotals) {

    var series = [],
        categories = [];

    $.each(categorySubtotals, function (i, obj) {
        categories.push(obj.category.toLowerCase());
    });
    categories.sort();

    $.each(categories, function (i, category) {
        var data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        $.each(days, function (date, expenses) {
            $.each(expenses, function (_, e) {
                // -1 to convert month to array index.
                if (e.category == category) {
                    var month = parseInt(date.split('-')[1]) - 1;
                    data[month] += e.cost;
                }
            });
        });
        series.push({
            name: category,
            data: data
        });
    });

    $('#categories-by-month-container').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Expenses by category by month'
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total monthly expenses'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                lineWidth: 1
            }
        },
        series: series
    });
};
