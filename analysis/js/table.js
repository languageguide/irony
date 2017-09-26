$(function() {
    $.getJSON('./json/ttest.json', function (object) {

        $('#example').DataTable( object );

    });
});
