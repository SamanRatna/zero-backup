var r=100;
var cf= 2*Math.PI*r;
var semi_cf = cf/2;
var topSpeed = 120;
var averageSpeedDash = document.getElementById('av-speed-meter');
var averageSpeedValue = document.getElementById('av-speed-value');

function setAverageSpeed(speed){
    var gaugeValue = ((speed * cf) / topSpeed);
    averageSpeedDash.setAttribute("stroke-dasharray", gaugeValue + "," + cf);
    // averageSpeedValue.innerHTML = speed;
}
// setAverageSpeed(60);