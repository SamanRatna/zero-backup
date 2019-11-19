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

// eel.expose(updateLeftTurnStatus);
function updateLeftTurnStatus(arg) {
    leftTurnStatus = arg;
}

// eel.expose(updateRightTurnStatus);
function updateRightTurnStatus(arg) {
    rightTurnStatus = arg;
}

// eel.expose(updateHighBeamStatus);
function updateHighBeamStatus(arg) {
    highBeamValue = arg;
}

//eel.expose(updateTripDistance);
function updateTripDistance(argA, argB) {
    tripDistanceA = argA;
    tripDistanceB = argB;
}

eel.expose(updateSpeedPower);
function updateSpeedPower(speed, power) {
    setSpeed(speed);
    document.getElementById('power-status-value').innerHTML = power;
    console.log('CAN: Speed= '+speed+ ' Power= '+ power)
}
eel.expose(updateSOC);
function updateSOC(soc) {
    document.getElementById('soc-status-value').innerHTML = soc;
    console.log('CAN: SOC= '+ soc)
}