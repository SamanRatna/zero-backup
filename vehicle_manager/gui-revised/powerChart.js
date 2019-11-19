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
            data: [10, 12, 15, 17, 18, 17, 16, 12, 13, 10, 12, 15, 17, 18, 17, 16, 12, 13, 12, 15, 17, 18, 17, 3000]
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
                    max: 120,
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
    }
});

function addData(chart, label, data) {
    if(chart.data.labels.length >= 25){
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
    setPowerChartPopup(data);
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

let currentPosition = 75;
let maxPower = 120
function setPowerChartPopup(power){
    var position = 75 - (power/maxPower*50);
    gotoPosition(position);
}

let positionMode = 1;
function gotoPosition(newPosition){
    value = newPosition + "%";
    document.documentElement.style.setProperty('--powerPopTopNew', value);
    if(positionMode==1){
        document.getElementById("power-pop").style.animation = "powerPopPosition1 0.3s 1 normal forwards";
        positionMode=2;
    }
    else if(positionMode==2){
        document.getElementById("power-pop").style.animation = "powerPopPosition2 0.3s 1 normal forwards";
        positionMode=1;
    }
    setTimeout(function(){
    document.documentElement.style.setProperty('--powerPopTopOld', value);
    }, 250)
}

