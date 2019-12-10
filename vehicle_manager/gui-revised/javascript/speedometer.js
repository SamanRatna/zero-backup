var rOdo=88;
var rTrip=156;
var rMax=225;

var cfOdo= 2*Math.PI*rOdo;
var cfTrip= 2*Math.PI*rTrip;
var cfMax= 2*Math.PI*rMax;

var scfOdo = cfOdo/2;
var scfTrip = cfTrip/2;
var scfMax = cfMax/2;

var topSpeed = 120;
var odoSpeedMeter = document.getElementById('odo-speed-meter');
var tripSpeedMeter = document.getElementById('trip-speed-meter');
var maxSpeedMeter = document.getElementById('max-speed-meter');

var odoSpeedValue = document.getElementById('value-odo-average')
var tripSpeedValue = document.getElementById('value-trip-average')
var maxSpeedValue = document.getElementById('value-max-speed')

var gaugeValue = 0;

function setAverageSpeed(max, odo, trip){
    gaugeValue = ((max * scfMax) / topSpeed);
    maxSpeedMeter.setAttribute("stroke-dasharray", gaugeValue + "," + cfMax);
    maxSpeedValue.innerHTML = max;

    gaugeValue = ((odo * scfOdo) / topSpeed);
    odoSpeedMeter.setAttribute("stroke-dasharray", gaugeValue + "," + cfOdo);
    odoSpeedValue.innerHTML = odo;

    gaugeValue = ((trip * scfTrip) / topSpeed);
    tripSpeedMeter.setAttribute("stroke-dasharray", gaugeValue + "," + cfTrip);
    tripSpeedValue.innerHTML = trip;
}
// setAverageSpeed(100, 50, 70);

function setMaxSpeed(max) {
    gaugeValue = ((max * scfMax) / topSpeed);
    maxSpeedMeter.setAttribute("stroke-dasharray", gaugeValue + "," + cfMax);
    maxSpeedValue.innerHTML = max;
}

function setAverageSpeeds(odo, trip) {
    gaugeValue = ((odo * scfOdo) / topSpeed);
    odoSpeedMeter.setAttribute("stroke-dasharray", gaugeValue + "," + cfOdo);
    odoSpeedValue.innerHTML = odo;

    gaugeValue = ((trip * scfTrip) / topSpeed);
    tripSpeedMeter.setAttribute("stroke-dasharray", gaugeValue + "," + cfTrip);
    tripSpeedValue.innerHTML = trip;
}