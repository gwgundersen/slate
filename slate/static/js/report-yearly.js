/* Additional functions for yearly reports.
 */

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
