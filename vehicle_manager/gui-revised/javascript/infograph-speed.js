let maxSpeed = null;
let odoAverage = null;
let tripAverage = null;
let maxSpeed_miles = null;
let odoAverage_miles = null;
let tripAverage_miles = null;
let unitIsKm = true;
const KM_TO_MILES = 0.621371;

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
    maxSpeed_miles = Math.floor(value*KM_TO_MILES)
    maxSpeed = value;
    if(unitIsKm){
        speedChart.data.datasets[0].data[0] = maxSpeed;
    } else {
        speedChart.data.datasets[0].data[0] = maxSpeed_miles;
    }
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
    odoAverage = odo;
    tripAverage = trip;
    odoAverage_miles = Math.floor(odo*KM_TO_MILES);
    tripAverage_miles = Math.floor(trip*KM_TO_MILES);

    if(unitIsKm){
        speedChart.data.datasets[0].data[1] = odoAverage;
        speedChart.data.datasets[0].data[2] = tripAverage;
    } else {
        speedChart.data.datasets[0].data[1] = odoAverage_miles;
        speedChart.data.datasets[0].data[2] = tripAverage_miles; 
    }
    speedChart.update();
}

function changeUnitToMiles(toMiles){
    if(unitIsKm != toMiles){
        return;
    } else {
        unitIsKm = !toMiles;
    }
    if(toMiles){
        if(maxSpeed_miles != null){
            speedChart.data.datasets[0].data[0] = maxSpeed_miles;
        }
        if(odoAverage_miles != null){
            speedChart.data.datasets[0].data[1] = odoAverage_miles;
        }
        if(tripAverage_miles != null){
            speedChart.data.datasets[0].data[2] = tripAverage_miles;
        }
    }else{
        if(maxSpeed != null){
            speedChart.data.datasets[0].data[0] = maxSpeed;
        }
        if(odoAverage != null){
            speedChart.data.datasets[0].data[1] = odoAverage;
        }
        if(tripAverage != null){
            speedChart.data.datasets[0].data[2] = tripAverage;
        }
    }
    speedChart.update();
}