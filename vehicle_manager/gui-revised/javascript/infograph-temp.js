var data = {
    labels: ["CONTROLLER", "ECU", "BATTERY", "AMBIENT", "MOTOR"],
    datasets: [{
        borderColor: 'rgba(48, 213, 200, 0.6)',
        borderWidth: 8,
        fill: true,
        backgroundColor: 'rgba(48, 213, 200, 0.2)',
        data: [0, 0, 0, 0, 0]
    }]
};

Chart.defaults.global.defaultFontColor = '#fff';

var options = {
    maintainAspectRatio: false,
    legend: {
        display: false
    },
    tooltips: {
        enabled: false
    },
    scale: {
        reverse: false,
        gridLines: {
            display: true,
            circular: true,
            lineWidth: 3
        },
        angleLines: {
            display: true,
            lineWidth: 3
        },
        ticks: {
            display: true,
            fontSize: 30,
            fontColor: '#666',
            fontFamily: 'Barlow',
            fontStyle: 'bold',
            stepSize: 25,
            beginAtZero: false,
            min: 1,
            max: 70,
            maxTicksLimit: 5,
            lineHeight: 50
        },
        pointLabels: {
            display: true,
            fontSize: 30,
            fontFamily: 'Barlow',
            fontStyle: 'bold',
            fontColor: '#666'
        },
    },
    elements: {
        point: {
              radius: 1,
              hitRadius: 20
        }
    }
};

var temperatureChart = new Chart('temperature-canvas', {
    type: 'radar',
    data: data,
    options: options
});

function changeBatteryTemperature(value) {
    temperatureChart.data.datasets[0].data[2] = value;
    temperatureChart.update();
}

eel.expose(updateMotorTemperature);
function updateMotorTemperature(motorTemp, controllerTemp){
    temperatureChart.data.datasets[0].data[4] = motorTemp;
    temperatureChart.data.datasets[0].data[0] = controllerTemp;
    temperatureChart.update();
}

// function changeControllerTemperature(value){
//     carbonChart.data.datasets[0].data[0] = value;
//     carbonChart.update();
// }
