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

setInterval(function () {
    // speed = Math.floor((Math.random() * 100) + 1);
    // speedGenerator();
    // document.getElementsByClassName("speed").innerHTML = speed;
    // document.getElementsByClassName("speedMain").innerHTML = speed;
    // addData(speedChart, "80s", speed);
    // document.getElementsByClassName("powerMain").innerHTML = Math.floor((Math.random() * 100) + 1);
    // document.getElementsByClassName("tripMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    // document.getElementsByClassName("lightMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    // document.getElementsByClassName("odoMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);

    // function leftTurnOnLoop() {
    //     setTimeout(function () {
    //         if (leftTurnStatus == 1) {
    //             document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOn.png";
    //             leftTurnOffLoop();
    //         }
    //     }, 300)
    // }


    // function leftTurnOffLoop() {
    //     setTimeout(function () {
    //         document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOff.png";
    //         if (leftTurnStatus == 1) {
    //             leftTurnOnLoop();
    //         }
    //     }, 300)
    // }


    // function rightTurnOnLoop() {
    //     setTimeout(function () {
    //         if (rightTurnStatus == 1) {
    //             document.getElementsByClassName("rightTurn")[0].src = "files/images/rightArrowOn.png";
    //             rightTurnOffLoop();
    //         }
    //     }, 300)
    // }


    // function rightTurnOffLoop() {
    //     setTimeout(function () {
    //         document.getElementsByClassName("rightTurn")[0].src = "files/images/rightArrowOff.png";
    //         if (rightTurnStatus == 1) {
    //             rightTurnOnLoop();
    //         }
    //     }, 300)
    // }

    // function highBeam() {
    //     if (highBeamStatus == 0) {
    //         document.getElementsByClassName("beam")[0].src = "files/images/highBeamOff.png";
    //     }
    //     else {
    //         document.getElementsByClassName("beam")[0].src = "files/images/highBeamOn.png";
    //     }
    // }
    // if (modeValue == 1) {
    //     document.getElementsByClassName("modeMain")[0].src = "files/images/mode1.png";
    // } else if (modeValue == 2) {
    //     document.getElementsByClassName("modeMain")[0].src = "files/images/mode2.png";
    // }
    // else {
    //     document.getElementsByClassName("modeMain")[0].src = "files/images/mode3.png";
    // }


    // leftTurnOffLoop();
    // leftTurnOnLoop();
    // rightTurnOffLoop();
    // rightTurnOnLoop();
    // highBeam();


    //     setInterval(100);
    //     document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOff.png";
    //     setInterval(100);



    // console.log(leftTurn=Math.round(Math.random()));
    // rightTurn=Math.round(Math.random());
    // document.getElementsByClassName("leftTurn")[0].src== "files/images/leftArrowOn.png";
}, 1500);

eel.expose(updateBikeMode);
function updateBikeMode(arg) {
    console.log(arg + ' from main');

    if(arg == "MODE_STANDBY"){
        document.getElementById("mode-notification").innerHTML = "STANDBY";
        setMode("standby");
    }
    else if(arg == "MODE_SUSTE"){
        modeValue = 1;
        document.getElementById("mode-notification").innerHTML = "SUSTE";
        setMode("thikka");
    }
    else if(arg == "MODE_THIKKA"){
        modeValue = 2;
        document.getElementById("mode-notification").innerHTML = "THIKKA";
        setMode("thikka");
    }
    else if(arg == "MODE_BABBAL"){
        modeValue = 3;
        document.getElementById("mode-notification").innerHTML = "BABBAL";
        setMode("babbal");
    }
    else if(arg == "MODE_REVERSE"){
        document.getElementById("mode-notification").innerHTML = "REVERSE";
        setMode("thikka");
    }
    else if(arg == "MODE_CHARGING"){
        //mylogo.src="files/images/logo_reverse.png";
        document.getElementById("mode-notification").innerHTML = "CHARGING";
    }
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
    document.getElementById('speed-value').innerHTML = speed;
    document.getElementById('babbal-speed-value').innerHTML = speed;
    document.getElementById('power-value').innerHTML = power;
    if(power < 0){
        document.getElementById("power-pop-value").innerHTML=0;
        addData(powerChart, "80s", 0);
    } else {
        document.getElementById("power-pop-value").innerHTML=speed;
        addData(powerChart, "80s", speed);
    }

    console.log('CAN: Speed= '+speed+ ' Power= '+ power)
}
eel.expose(updateSOC);
function updateSOC(soc) {
    document.getElementById('range-value').innerHTML = soc;
    console.log('CAN: SOC= '+ soc)
}