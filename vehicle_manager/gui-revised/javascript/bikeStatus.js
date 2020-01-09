var leftTurnStatus = 0;
var rightTurnStatus = 0;
var modeValue = 3;
var highBeamStatus = 0;
var speed = 0;
var tripDistanceA = 0;
var tripDistanceB = 0;

function sliderButtonVisibility(visibility){
    if(visibility == "on"){
        document.getElementById('slider-wrap').classList.add("active");
    }
    else if (visibility == "off") {
        document.getElementById('slider-wrap').classList.remove("active");
    }
}

function updateSpeed(speed){
    if(speed > 15){
        sliderButtonVisibility("off")
    }
    else{
        sliderButtonVisibility("on")
    }
}


eel.expose(updateBikeMode);
function updateBikeMode(arg) {
    console.log(arg + ' from main');
    setMode(arg);
}

let statusSpeed2 = document.getElementById('speed-status-value');
eel.expose(updateSpeedPower);
function updateSpeedPower(speed, power) {
    statusSpeed2.innerHTML = speed;
    setSpeed(speed);
    document.getElementById('power-status-value').innerHTML = power;
    // console.log('CAN: Speed= '+speed+ ' Power= '+ power)
}
eel.expose(updateSOC);
function updateSOC(soc, rangeSuste,rangeThikka, rangeBabbal) {
    document.getElementById('soc-status-value').innerHTML = soc;
    // document.getElementById('engg-battery-status').innerHTML = soc;
    document.getElementById('range-suste').innerHTML = rangeSuste;
    document.getElementById('range-thikka').innerHTML = rangeThikka;
    document.getElementById('range-babbal').innerHTML = rangeBabbal;
    // console.log('CAN: SOC= '+ soc)
}

eel.expose(updateOdometer)
function updateOdometer(odometer, tripOdo) {
    document.getElementById('odo-info-value').innerHTML = odometer;
    document.getElementById('trip-info-value').innerHTML = tripOdo;
}
eel.expose(updateChargingStatus);
function updateChargingStatus(status, current, timeToCharge) {
    // document.getElementById('engg-charging-status').innerHTML = status;
    // document.getElementById('engg-charging-current').innerHTML = current;
    // document.getElementById('engg-charge-time').innerHTML = timeToCharge;
}

eel.expose(updateSpeedInfograph);
function updateSpeedInfograph(maxSpeed, odoAverage, tripAverage) {
    console.log('updatingSpeedInfograph');
    setAverageSpeed(maxSpeed, odoAverage, tripAverage);
}

eel.expose(updateMaxSpeed);
function updateMaxSpeed(value){
    setMaxSpeed(value);
}

eel.expose(updateAverageSpeeds);
function updateAverageSpeeds(odo, trip){
    setAverageSpeeds(odo, trip);
}

eel.expose(updateDistances)
function updateDistances(odometer, tripOdo) {
    document.getElementById('odo-info-value').innerHTML = odometer;
    document.getElementById('trip-info-value').innerHTML = tripOdo;
}

eel.expose(updateBatteryTemperature);
function updateBatteryTemperature(temp){
    changeBatteryTemperature(temp);
}

eel.expose(updateMotorTemperature);
function updateMotorTemperature(temp){
    changeMotorTemperature(temp);
}

eel.expose(updateControllerTemperature);
function updateControllerTemperature(temp){
    changeControllerTemperature(temp);
}

function initiateTripReset(){
    eel.resetTripData()
}

function initializeGUI(){
    eel.getGUIData()
}

// eel.expose(updateGUIData)
// function updateGUIData(maxSpeed){
//     setMaxSpeed(maxSpeed);
// }
initializeGUI();
