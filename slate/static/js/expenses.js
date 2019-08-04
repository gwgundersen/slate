$(function() {
    $('table').DataTable({
        bPaginate: false,
        // Disables sorting on load while allowing column sorting.
        aaSorting: [],
        order: [[ 3, 'desc' ]]
    });
});