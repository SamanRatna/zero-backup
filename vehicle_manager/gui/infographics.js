var r=100;
var cf= 2*Math.PI*r;
var semi_cf = cf/2;
var topSpeed = 120;
var averageSpeedDash = document.getElementById('av-speed-meter');
var averageSpeedValue = document.getElementById('av-speed-value');

function setAverageSpeed(speed){
    var gaugeValue = ((speed * cf) / topSpeed);
    averageSpeedDash.setAttribute("stroke-dasharray", gaugeValue + "," + cf);
    averageSpeedValue.innerHTML = speed;
}

// function successCircle(val){
//     var r=114.5;
//     var cf= 2*Math.PI*r;
//     var semi_cf = cf/2;
//     var circleValue = val;
//     document.getElementById("svg_1").setAttribute("stroke-dasharray", circleValue + "," + cf);
// }

// setInteval
var totalDistanceValue = document.getElementById("total-distance-value");
function setTotalDistance(distance){
    totalDistanceValue.innerHTML = distance;
}

var trip_a_bg = document.getElementById("trip-a-button-hlight");
var trip_a_switch = document.getElementById("trip-a-switch");
var trip_b_bg = document.getElementById("trip-b-button-hlight");
var trip_b_switch = document.getElementById("trip-b-switch");
var trip_a = "off";
var trip_b = "off";
function toggleTrip(trip){
    // console.log("Trip: " + trip);
    if(trip == 'a'){
        if(trip_a == "off"){
            trip_a_bg.style.animation = "activate-trip-bg 0.2s 1 ease-out forwards";
            trip_a_switch.style.animation = "activate-trip-switch 0.2s 1 ease-out forwards";
            trip_a = "on";
        }
        else if(trip_a == "on"){
            trip_a_bg.style.animation = "deactivate-trip-bg 0.2s 1 ease-in normal forwards";
            trip_a_switch.style.animation = "deactivate-trip-switch 0.2s 1 ease-in normal forwards";
            trip_a = "off";
        }
    }
    else if(trip == 'b'){
        if(trip_b == "off"){
            trip_b_bg.style.animation = "activate-trip-bg 0.2s 1 ease-out forwards";
            trip_b_switch.style.animation = "activate-trip-switch 0.2s 1 ease-out forwards";
            trip_b="on";
        }
        else if(trip_b == "on"){
            trip_b_bg.style.animation = "deactivate-trip-bg 0.2s 1 ease-out normal forwards";
            trip_b_switch.style.animation = "deactivate-trip-switch 0.2s 1 ease-out normal forwards";
            trip_b = "off";
        }
    }
}

var tripsCard = document.getElementById("infocard-trips");
tripsCard.addEventListener("longtap", function(){
    //open trip reset modal
    console.log("Reset Trips");
    openTripResetModal();
});

let resetInProgress="no";
function resetTrip(trip="both"){
    
    if(resetInProgress == "yes"){
        return;
    }

    resetInProgress = "yes";
    activateTripReset(trip);

    setTimeout(function(){
        closeModal();
        deactivateTripReset(trip);
    }, 3000);
}

function activateTripReset(trip){
    if(trip == "a"){
        document.getElementById("modal-trip-b").style.color = "rgb(200, 200, 200)";
        document.getElementById("modal-both-trips").style.color = "rgb(200, 200, 200)";
        document.getElementById("trip-a-reset-success").style.display = "block";
    }
    else if(trip=="b"){
        document.getElementById("modal-trip-a").style.color = "rgb(200, 200, 200)";
        document.getElementById("modal-both-trips").style.color = "rgb(200, 200, 200)";
        document.getElementById("trip-b-reset-success").style.display = "block";
    }
    else if(trip=="both"){
        document.getElementById("modal-trip-a").style.color = "rgb(200, 200, 200)";
        document.getElementById("modal-trip-b").style.color = "rgb(200, 200, 200)";
        document.getElementById("trip-both-reset-success").style.display = "block";
    }
}

function deactivateTripReset(trip){
    if(trip == "a"){
        document.getElementById("modal-trip-b").style.color = "black";
        document.getElementById("modal-both-trips").style.color = "black";
        document.getElementById("trip-a-reset-success").style.display = "none";
    }
    else if(trip=="b"){
        document.getElementById("modal-trip-a").style.color = "black";
        document.getElementById("modal-both-trips").style.color = "black";
        document.getElementById("trip-b-reset-success").style.display = "none";
    }
    else if(trip=="both"){
        document.getElementById("modal-trip-a").style.color = "black";
        document.getElementById("modal-trip-b").style.color = "black";
        document.getElementById("trip-both-reset-success").style.display = "none";
    }
    resetInProgress="no";
}

var batteryTemp = 25;
var tempValue = document.getElementById('battery-temp');
var thermoLevel = document.getElementById('thermometer-level');
function setBatteryTemp(temp){
    tempValue.innerHTML = temp;
    tLevel = temp / 50 *100;
    thermoLevel.style.width = tLevel + "%";
}