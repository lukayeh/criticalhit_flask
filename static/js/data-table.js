$(document).ready(function(){
 $('#roster-table').DataTable({
    language: {
        search: "_INPUT_",
        searchPlaceholder: "Search..",
    }
});
});

$(document).ready(function(){
    $('#generic-table').DataTable({
       language: {
           search: "_INPUT_",
           searchPlaceholder: "generic..",
       },
       "paging": false,
       "searching": false,
});
});