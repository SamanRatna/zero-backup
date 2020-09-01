var data = {
    labels: ["MAX SPEED", "ODO AVERAGE", "TRIP AVERAGE"],
    datasets: [{
        fill: true,
        backgroundColor: ['rgba(7,147,136,1)',
                            'rgba(48,213,200,1)',
                            'rgba(176,255,249,1)'],
        data: [0, 0, 0]
    }]
};

Chart.defaults.global.defaultFontColor = '#C4C4C4;';
Chart.defaults.global.defaultFontFamily = 'Barlow';
var options = {
    maintainAspectRatio: false,
    legend: {
        display: false,
        // labels: {
        //     // fontStyle: 'Barlow'
        //     fontColor: '#C4C4C4',
        // }
    },
    tooltips: {
        enabled: false
    },
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true,
                maxTicksLimit: 5,
                fontSize: 30,
                fontColor: '#C4C4C4'
            },
            gridLines: {
                drawBorder: false,
                zeroLineWidth: 6,
                zeroLineColor: 'rgba(196, 196, 196, 1)',
                // borderDashOffset: 20,
            }
        }],
        xAxes: [{
            gridLines: {
                display: false,
                drawBorder: false,
            },
            ticks:{
                fontSize: 25,
                fontColor: '#C4C4C4'
            }
        }],
    },
};

var speedChart = new Chart('speed-canvas', {
    type: 'bar',
    data: data,
    options: options
});


function updateMaxSpeed(value) {
    speedChart.data.datasets[0].data[0] = value;
    speedChart.update();
}

// function changeOdoAverage(value){
//     speedChart.data.datasets[0].data[1] = value;
//     speedChart.update();
// }

// function changeTripAverage(value){
//     speedChart.data.datasets[0].data[2] = value;
//     speedChart.update();
// }

function updateAverageSpeeds(odo, trip){
    speedChart.data.datasets[0].data[1] = odo;
    speedChart.update();  
    speedChart.data.datasets[0].data[2] = trip;
    speedChart.update();
}