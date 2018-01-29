$(function() {

    var ctx1 = document.getElementById("summaryChart");
    var ctx2 = document.getElementById("correctResponse");
    var ctx3 = document.getElementById("correctResponseByContext");
    var ctx4 = document.getElementById("correctResponseByIrony");

    options = {
        legend: {
            labels: {
                fontSize: 22
            }
        },
        pieceLabel: {
            render: 'percentage',
            precision: 1,
            fontSize: 16,
            arc: true,
            fontColor: 'white'
        }
    }

    $.getJSON("json/summary.json", function (object) {
        var myChart = new Chart(ctx1, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: Object.values(object),
                    backgroundColor: ["#7FDBFF", "#39CCCC","#01FF70","#e8c3b9","#2ECC40"]
                }],
                labels: Object.keys(object)
            },
            options: options
        });
    });
    $.getJSON("json/correctResponse.json", function (object) {
        var myChart = new Chart(ctx2, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: Object.values(object),
                    backgroundColor: ["#FF4136", "#01FF70"]
                }],
                labels: Object.keys(object)
            },
            options: options
        });
    });
    $.getJSON("json/correctResponseByContext.json", function (object) {
        var myChart = new Chart(ctx3, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: Object.values(object),
                    backgroundColor: ["#FF4136", "#01FF70","#e8c3b9","#2ECC40"]
                }],
                labels: Object.keys(object)
            },
            options: options
        });
    });
    $.getJSON("json/correctResponseByIrony.json", function (object) {
        var myChart = new Chart(ctx4, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: Object.values(object),
                    backgroundColor: ["#FF4136", "#01FF70","#e8c3b9","#2ECC40"]
                }],
                labels: Object.keys(object)
            },
            options: options
        });
    });

});

