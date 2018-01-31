$(function() {

    $.ajaxSetup({ cache: false });

    $.getJSON('./json/ttest.json', function (object) {

        $('#example').DataTable( object );

    });

    $.getJSON('./json/ttestByIronyType.json', function (object) {

        $('#trials1-irony').DataTable( object );

    });

    $.getJSON('./json/ttest_tr1_tr2_ironyType.json', function (object) {
        console.log(object);

        $('#tr1-tr2-irony').DataTable( object );

    });

});
