$(function() {

    var ctx = document.getElementById("userResponse");

    $.getJSON("json/userResponse.json", function (object) {

        var keys = Object.keys(object)
        var values = Object.values(object)
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                // TODO fix with lenght of the object
                labels: [...Array(30).keys()],
                // TODO fix with a loop
                datasets: [
                    {
                        label: keys[0],
                        backgroundColor: "#D1F2EB",
                        data: values[0]
                    }, {
                        label: keys[1],
                        backgroundColor: "#FCF3CF",
                        data: values[1]
                    }, {
                        label: keys[2],
                        backgroundColor: "#EBDEF0",
                        data: values[2]
                    }, {
                        label: keys[3],
                        backgroundColor: "#FBEEE6",
                        data: values[3]
                    }
                ]
            },
            options: {
                tooltips: {
                    mode: 'index',
                    intersect: false
                },
                responsive: true,
                scales: {
                    xAxes: [{
                        stacked: true,
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                },
                legend: {
                    labels: {
                        fontSize: 22
                    }
                }
            }
        });

    });
});

