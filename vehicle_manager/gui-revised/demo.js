// Babbal Speed Value in Babbal Slide
// setInterval( function(){
//     document.getElementById('babbal-speed-value').innerHTML = Math.floor((Math.random() * 100) + 1);
// }, 250)

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
}

function randomPowerGenerator(){
    var randNum = (Math.random() + Math.random()) / 2; 
    var randNum = (Math.random() + Math.random() + Math.random()) / 3; 
    var randNum = (Math.random() + Math.random() + Math.random() + Math.random()) / 4 * 35; 
    return Math.floor(randNum);
}

setInterval(function(){   
    speedGenerator();
    hp = randomPowerGenerator();
    //document.getElementById("speed-value").innerHTML=speed;
    // addData(speedChart, "80s", speed);
    // updateSpeed(speed);
    //addData(powerChart, "80s", hp);
    // setPowerChartPopup(hp);
    // updateSpeed(speed);
    //rangeDemo();
    //document.getElementById("power-value").innerHTML=hp;
    //document.getElementById("power-pop-value").innerHTML=hp;
    //document.getElementsByClassName("rangeMain").innerHTML = Math.floor((Math.random() * 100) + 1);
    totalDistanceDemo();
    batteryTempDemo();
}, 500);

setInterval(function(){   
    batteryTempDemo();
    avSpeedDemo();
}, 30);

setInterval(function(){   
    tripDemo();
}, 1500);

// Indicators demo
setInterval(function () {
    let rturn = Math.round(Math.random());
    let lturn = Math.round(Math.random());
    let beam = Math.round(Math.random());

    if(rturn==1 && lturn==1){
        document.getElementById("rightTurn").src = "files/images/rightArrowOff.png";
        document.getElementById("leftTurn").src = "files/images/leftArrowOff.png";
    }
    else{
        if(rturn == 0){
            document.getElementById("rightTurn").src = "files/images/rightArrowOff.png";
        }
        else{
            document.getElementById("rightTurn").src = "files/images/rightArrowOn.png";
        }
    
        if(lturn == 0){
            document.getElementById("leftTurn").src = "files/images/leftArrowOff.png";
        }
        else{
            document.getElementById("leftTurn").src = "files/images/leftArrowOn.png";
        }
    }
    

    if(beam == 0){
        document.getElementById("beam").src = "files/images/highBeamOff.png";
    }
    else{
        document.getElementById("beam").src = "files/images/highBeamOn.png";
    }

}, 1500);