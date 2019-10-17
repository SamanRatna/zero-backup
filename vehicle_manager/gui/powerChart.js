var ctx = document.getElementById('power-chart').getContext("2d");
var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
gradientStroke.addColorStop(0, "rgba(64,224,208, 0.6)");
gradientStroke.addColorStop(0.5, "rgba(64,224,208,0.4)");
gradientStroke.addColorStop(1, "rgba(64,224,208,0.1)");

var gradientFill = ctx.createLinearGradient(0, 0, 0, 600);
gradientFill.addColorStop(0, "rgba(64,224,208, 1)");
gradientFill.addColorStop(0.5, "rgba(64,224,208,0.5)");
gradientFill.addColorStop(0.8, "rgba(64,224,208,0.1)");
gradientFill.addColorStop(1, "rgba(64,224,208,0)");

var powerChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["0", "1", "2", "3", "4", "5", "6", "7", "0", "1", "2", "3", "4", "5", "6", "7", "0", "1", "2", "3", "4", "5", "6", "7"],
        datasets: [{
            label: "Data",
            borderColor: gradientStroke,
            pointBorderColor: gradientStroke,
            pointBackgroundColor: gradientStroke,
            pointHoverBackgroundColor: gradientStroke,
            pointHoverBorderColor: gradientStroke,
            pointBorderWidth: 1,
            pointHoverRadius: 10,
            pointHoverBorderWidth: 1,
            pointRadius: 0,
            fill: true,
            backgroundColor: gradientFill,
            borderWidth: 0,
            data: [10, 12, 15, 17, 18, 17, 16, 12, 13, 10, 12, 15, 17, 18, 17, 16, 12, 13, 12, 15, 17, 18, 17, 16]
        }]
    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
        legend: {
            position: "bottom",
            display: false
        },
        scales: {
            yAxes: [{
                ticks: {
                    fontColor: "rgba(0,0,0,0.5)",
                    fontStyle: "bold",
                    beginAtZero: true,
                    maxTicksLimit: 5,
                    padding: 20,
                    display: false
                },
                gridLines: {
                    drawTicks: false,
                    display: false
                }
}],
            xAxes: [{
                gridLines: {
                    zeroLineColor: "transparent",
                    display: false
},
                ticks: {
                    padding: 20,
                    fontColor: "rgba(0,0,0,0.5)",
                    fontStyle: "bold",
                    display: false
                }
            }]
        },
        // tooltips: {
        //     mode: 'index',
        //     intersect: false,
        //     bodyFontSize: 50
        //   },
        //  hover: {
        //     mode: 'nearest',
        //     intersect: true
        //   },
    }
});

function addData(chart, label, data) {
    if(chart.data.labels.length = 25){
        chart.data.labels.shift();
        chart.data.labels.push(label);
    }
    
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
        if(dataset.data.length >= 25){
            dataset.data.shift();
        }
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}