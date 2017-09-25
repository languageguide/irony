$(function() {

    var ctx = document.getElementById("summaryChart");

    $.getJSON("json/summary.json", function (object) {
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: Object.values(object),
                    backgroundColor: ["#7FDBFF", "#39CCCC","#01FF70","#e8c3b9","#2ECC40"]
                }],
                labels: Object.keys(object)

            },
            options: {
                legend: {
                    labels: {
                        fontSize: 22
                    }
                },
                pieceLabel: {
                    render: 'percentage',
                    precision: 2,
                    fontSize: 18,
                    arc: true
                }
            }
        });

    });
});

