var leftTurnStatus = 1;
var rightTurnStatus = 0;
var modeValue = 3;
var highBeamStatus = 0;

eel.expose(updateBikeMode);
function updateBikeMode(arg) {
    console.log(arg + ' from main');
    mylogo = document.getElementById('logo');

    if(arg == "MODE_STANDBY"){
        //mylogo.src="files/images/logo_standby.png";
    }
    else if(arg == "MODE_SUSTE"){
        modeValue = 1;
    }
    else if(arg == "MODE_THIKKA"){
        modeValue = 2;
    }
    else if(arg == "MODE_BABBAL"){
        modeValue = 3;
    }
    else if(arg == "MODE_CHARGING"){
        //mylogo.src="files/images/logo_reverse.png";
    }
}

eel.expose(updateLeftTurnStatus);
function updateLeftTurnSignal(arg) {
    leftTurnStatus = arg;
}

eel.expose(updateRightTurnStatus);
function updateRightTurnSignal(arg) {
    rightTurnStatus = arg;
}

eel.expose(updateHighBeamStatus);
function updateHighBeamStatus(arg) {
    highBeamValue = arg;
}

setInterval(function () {
    document.getElementsByClassName("speed")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("speedMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("powerMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("rangeMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    // document.getElementsByClassName("tripMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    // document.getElementsByClassName("lightMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    // document.getElementsByClassName("odoMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);

    function leftTurnOnLoop() {
        setTimeout(function () {
            if (leftTurnStatus == 1) {
                document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOn.png";
                leftTurnOffLoop();
            }
        }, 300)
    }


    function leftTurnOffLoop() {
        setTimeout(function () {
            document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOff.png";
            if (leftTurnStatus == 1) {
                leftTurnOnLoop();
            }
        }, 300)
    }


    function rightTurnOnLoop() {
        setTimeout(function () {
            if (rightTurnStatus == 1) {
                document.getElementsByClassName("rightTurn")[0].src = "files/images/rightArrowOn.png";
                rightTurnOffLoop();
            }
        }, 300)
    }


    function rightTurnOffLoop() {
        setTimeout(function () {
            document.getElementsByClassName("rightTurn")[0].src = "files/images/rightArrowOff.png";
            if (rightTurnStatus == 1) {
                rightTurnOnLoop();
            }
        }, 300)
    }

    function highBeam() {
        if (highBeamStatus == 0) {
            document.getElementsByClassName("beam")[0].src = "files/images/highBeamOff.png";
        }
        else {
            document.getElementsByClassName("beam")[0].src = "files/images/highBeamOn.png";
        }
    }
    if (modeValue == 1) {
        document.getElementsByClassName("modeMain")[0].src = "files/images/mode1.png";
    } else if (modeValue == 2) {
        document.getElementsByClassName("modeMain")[0].src = "files/images/mode2.png";
    }
    else {
        document.getElementsByClassName("modeMain")[0].src = "files/images/mode3.png";
    }


    leftTurnOffLoop();
    leftTurnOnLoop();
    rightTurnOffLoop();
    rightTurnOnLoop();
    highBeam();


    //     setInterval(100);
    //     document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOff.png";
    //     setInterval(100);



    // console.log(leftTurn=Math.round(Math.random()));
    // rightTurn=Math.round(Math.random());
    // document.getElementsByClassName("leftTurn")[0].src== "files/images/leftArrowOn.png";
}, 1500);