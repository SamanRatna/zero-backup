// Babbal Speed Value in Babbal Slide
setInterval( function(){
    document.getElementById('babbal-speed-value').innerHTML = Math.floor((Math.random() * 100) + 1);
}, 250)

//Speed Generator Function
var dMode = 0;
function speedGenerator(){
    if(dMode == 0){
        speed = (speed + 2)
        if(speed > 97){
            dMode=1;
        }
    }
    else if(dMode == 1){
        speed = speed - 3;
        if(speed < 10){
            dMode = 0;
        }
    }
}

// Total Distance Demo
var dTotalDistance= 0;
function totalDistanceDemo(){
    if(dTotalDistance < 599){
        dTotalDistance += 4;
    }
    else{
        dTotalDistance = 0;
    }
    setTotalDistance(dTotalDistance);
}

// Battery Demo
var dBatteryTemp=15;
var dBatteryMode = 0;
function batteryTempDemo(){
    if(dBatteryMode == 0){
        if(dBatteryTemp < 49){
            dBatteryTemp += 1;
        }
        else{
            dBatteryTemp -= 1;
            dBatteryMode = 1;
        }
    }
    else {
        if(dBatteryTemp > 14){
            dBatteryTemp -= 1;
        }
        else{
            dBatteryTemp += 1;
            dBatteryMode = 0;
        }
    }
    setBatteryTemp(dBatteryTemp);
}

// Trip Distance Toggle Demo
var dTripMode = 0;
function tripDemo(){
    if(dTripMode == 0){
        toggleTrip('a');
        dTripMode = 1;
    }
    else if(dTripMode == 1){
        toggleTrip('b');
        dTripMode = 2;
    }
    else if(dTripMode == 2){
        toggleTrip('b');
        dTripMode = 3;
    }
    else if(dTripMode == 3){
        toggleTrip('b');
        toggleTrip('a');
        dTripMode = 0;
    }
}

// Trip Distance Demo
function tripDistanceDemo(){
    
}
// Average Speed Demo
var dAvSpeedMode = 0;
var dAvSpeed = 0;
function avSpeedDemo(){
    if(dAvSpeedMode == 0){
        if(dAvSpeed < 118){
            dAvSpeed += 1;
        }
        else{
            dAvSpeed -= 1;
            dAvSpeedMode = 1;
        }
    }
    else {
        if(dAvSpeed > 1){
            dAvSpeed -= 1;
        }
        else{
            dAvSpeed += 1;
            dAvSpeedMode = 0;
        }
    }
    setAverageSpeed(dAvSpeed);
}

// Range Value Demo
var dRange = 20;
function rangeDemo(){
    dRange = Math.floor((Math.random()*100)+1);
    document.getElementById("range-value").innerHTML= dRange;
    // document.getElementById("pop-range-suste").innerHTML = (dRange * 0.8).toFixed(0);
    // document.getElementById("pop-range-thikka").innerHTML = (dRange * 1.2).toFixed(0);
    // document.getElementById("pop-range-babbal").innerHTML = (dRange * 0.6).toFixed(0);
}

setInterval(function(){   
    speedGenerator();
    //document.getElementsByClassName("speed")[0].innerHTML=Math.floor((Math.random()*100)+1); 
    document.getElementById("speed-value").innerHTML=speed;
    addData(speedChart, "80s", speed);
    // updateSpeed(speed);
    rangeDemo();
    document.getElementById("power-value").innerHTML=Math.floor((Math.random()*100)+1); 
    document.getElementById("babbal-range-value").innerHTML=Math.floor((Math.random()*100)+1);
    document.getElementById("top-speed-value").innerHTML=Math.floor((Math.random()*100)+1);
    document.getElementsByClassName("rangeMain").innerHTML = Math.floor((Math.random() * 100) + 1);
    totalDistanceDemo();
    batteryTempDemo();
}, 300);

setInterval(function(){   
    batteryTempDemo();
    avSpeedDemo();
}, 30);

setInterval(function(){   
    tripDemo();
}, 1500);