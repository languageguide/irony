$(function() {

    $.ajaxSetup({ cache: false });

    $.getJSON('./json/ttest.json', function (object) {
        $('#example').DataTable( object );
    });

    $.getJSON('./json/ttestByIronyType.json', function (object) {
        $('#trials1-irony').DataTable( object );
    });

    $.getJSON('./json/ttest_tr1_tr2_ironyType.json', function (object) {
        $('#tr1-tr2-irony').DataTable( object );
    });

    $.getJSON('./json/negContVsPosCont.json', function (object) {
        $('#negContVsPosCont').DataTable( object );
    });

    $.getJSON('./json/liter_vs_ironic.json', function (object) {
        $('#liter-vs-ironic').DataTable( object );
    });

negContVsPosCont
});
