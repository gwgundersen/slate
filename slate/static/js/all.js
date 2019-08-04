$(function() {
    var $table = $('table').first(),
        config;
    config = {
        iDisplayLength: 200,
        bPaginate: true,
        oLanguage: {
            sSearch: 'Filter'
        },
        // Disables sorting on load while allowing column sorting.
        aaSorting: [],
        order: [[ 3, 'desc' ]],
        fnInitComplete: function() {
            // Set width to 100% because DataTables cannot seem to correctly
            // set the width when table is hidden.
            $table.css('width', '100%').fadeIn();
        }
    };
    $table.dataTable(config);
});