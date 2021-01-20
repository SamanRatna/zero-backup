let tController = null;
let tECU = null;
let tBattery = null;
let tAmbient = null;
let tMotor = null;
let tUnitIsCelsius = true;

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

eel.expose(updateBatteryTemperature);
function updateBatteryTemperature(value) {
    if(!tUnitIsCelsius){
        value = value * 9/5 +32
    }
    temperatureChart.data.datasets[0].data[2] = value;
    tBattery = value;
    temperatureChart.update();
}
eel.expose(updateVCUTemperature);
function updateVCUTemperature(uc, power) {
    // console.log('Unit is Celsius: '+tUnitIsCelsius);
    if(!tUnitIsCelsius){
        uc = uc * 9/5 +32;
        power = power * 9/5 +32
    }
    temperatureChart.data.datasets[0].data[1] = power;
    tECU = power;
    temperatureChart.data.datasets[0].data[3] = uc;
    tAmbient = uc;
    temperatureChart.update();
}
eel.expose(updateMotorTemperature);
function updateMotorTemperature(motorTemp, controllerTemp){
    if(!tUnitIsCelsius){
        motorTemp = motorTemp * 9/5 +32
        controllerTemp = controllerTemp * 9/5 +32
    }
    temperatureChart.data.datasets[0].data[4] = motorTemp;
    temperatureChart.data.datasets[0].data[0] = controllerTemp;
    tController = controllerTemp;
    tMotor = motorTemp;
    temperatureChart.update();
}

function changeUnitsToFarenheit(toFarenheit){
    console.log('Changing uints to Farenheit: ' + toFarenheit)
    if(tUnitIsCelsius != toFarenheit){
        return;
    } else {
        tUnitIsCelsius = !toFarenheit;
    }
    // console.log('Unit is Celsius: '+tUnitIsCelsius);

    if(toFarenheit){
        if(tController != null){
            tController = tController * 9/5 +32;
            temperatureChart.data.datasets[0].data[0] = tController;
        }
        if(tECU != null){
            tECU = tECU * 9/5 +32;
            temperatureChart.data.datasets[0].data[1] = tECU;
        }
        if(tBattery != null){
            tBattery = tBattery * 9/5 +32;
            temperatureChart.data.datasets[0].data[2] = tBattery;
        }
        if(tAmbient != null){
            tAmbient = tAmbient * 9/5 +32;
            temperatureChart.data.datasets[0].data[3] = tAmbient;
        }
        if(tMotor != null){
            tMotor = tMotor * 9/5 +32;
            temperatureChart.data.datasets[0].data[4] = tMotor;
        }
    }
    else{
        if(tController != null){
            tController = (tController -32)*5/9 ;
            temperatureChart.data.datasets[0].data[0] = tController;
        }
        if(tECU != null){
            tECU = (tECU -32)*5/9;
            temperatureChart.data.datasets[0].data[1] = tECU;
        }
        if(tBattery != null){
            tBattery = (tBattery -32)*5/9;
            temperatureChart.data.datasets[0].data[2] = tBattery;
        }
        if(tAmbient != null){
            tAmbient = (tAmbient -32)*5/9;
            temperatureChart.data.datasets[0].data[3] = tAmbient;
        }
        if(tMotor != null){
            tMotor = (tMotor -32)*5/9;
            temperatureChart.data.datasets[0].data[4] = tMotor;
        }
    }

    temperatureChart.update();
    // printTemperatures();
}

// function changeControllerTemperature(value){
//     carbonChart.data.datasets[0].data[0] = value;
//     carbonChart.update();
// }

// function printTemperatures(){
//     console.log('ECU Temperature: '+tECU);
// }