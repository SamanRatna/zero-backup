let bikeMode="standby";
let greeter = "on";
let indicators = "off";
let keyboard = "closed";
let internet = "off";

myGreeter = document.getElementById("greeter-1");
myStatus = document.getElementById("yatri-estate-2")
myIndicators = document.getElementById("indicator");
mySpeed = document.getElementById("status-speed");
myPower = document.getElementById("status-power");
myRange = document.getElementById("range-value");
myMap = document.getElementById("slide");
myHeartbeat = document.getElementById("babbal-speed");
myBabbalInfo = document.getElementById("babbal-info");
myLogoContainer = document.getElementById("yatri-logo-2");
myLogo = document.getElementById("yatri-logo-1");
myStatusRange = document.getElementById('status-range');
myRangeUnit = document.getElementById('range-unit');

function shrinkRange(){
    // myStatusRange.style.animation = "shrinking-status-range-width 0.2s 1 ease-out normal forwards";
    myRange.style.animation = "shrinking-range-value-font 0.2s 1 ease-out normal forwards";
    myRangeUnit.style.animation = "shrinking-range-unit-margin 0.2s 1 ease-out normal forwards";
}

function toggleKeyboard(){
    if(bikeMode == "babbal"){
        return;
    }

    //Opening the keyboard
    if(keyboard=='closed'){
        console.log("Opening Keyboard");
        if(myKeyboard != null){
            keyboard = 'open';
            // if(pos == 0){
            //     slideLeft();
            // }
            if(bikeMode == "standby"){
                myStatus.style.animation ="vanishingStatusInStandby 0.5s 1 ease-out forwards";
            }
            else if(bikeMode == "thikka"){
                myStatus.style.animation ="vanishingStatus 0.5s 1 ease-out forwards";
                document.getElementById("status-2").style.animation = "vanishingStatusPadding 0.5s 1 ease-out forwards";
            }

            if(greeter == "on"){
                myGreeter.style.animation = "vanishingGreeter 0.5s 1 ease-out normal forwards";
                greeter = "off";
            }
        }
    }

    //Closing the keyboard
    else if(keyboard =='open'){
        console.log("Closing Keyboard");
        if(myKeyboard != null){
            if(bikeMode == "thikka"){
                myStatus.style.animation ="appearingStatus 0.5s 1 ease-out forwards";
                document.getElementById("status-2").style.animation = "appearingStatusPadding 0.5s 1 ease-out forwards";
            }
            else if(bikeMode == "standby"){
                myStatus.style.animation ="appearingStatusInStandby 0.5s 1 ease-out forwards";
            }
            if(greeter == "off" && bikeMode=="standby"){
                myGreeter.style.animation = "appearingGreeter 0.5s 1 ease-out normal forwards";
                greeter = "on";
            }

            keyboard = 'closed';
        }
    }
}

function setMode(mode){
    if(mode == bikeMode){
        return;
    }
    if(bikeMode=="babbal" && mode == "standby"){
        myMap.style.animation = "appearingMap 0.5s 1 ease-out normal forwards";
        myHeartbeat.style.animation = "vanishingHeartbeat 0.5s 1 ease-out normal forwards";
    }
    
    // Go to STANDBY Mode
    if(mode=="standby"){
        if(bikeMode=="thikka"){
            // myRange.style.animation = "rangeEnlarge 0.5s 1 ease-out normal forwards";
            mySpeed.style.animation = "vanishingExtraStatus 0.5s 1 ease-out normal forwards";
            myPower.style.animation = "vanishingExtraStatus 0.5s 1 ease-out normal forwards";
            if(keyboard == "closed"){
                myIndicators.style.animation = "vanishingIndicatorsOpacity 0.5s 1 ease-out normal forwards"
                myStatus.style.animation = "vanishingIndicators 0.5s 1 ease-out normal forwards"
                if(greeter == "off"){
                    myGreeter.style.animation = "appearingGreeter 0.5s 1 ease-out normal forwards";
                    greeter = "on";
                }
                indicators = "off";
            }
            else if(keyboard == "open"){
                document.getElementById("status-2").style.animation = "appearingStatusPadding 0.5s 1 ease-out forwards";
            }
        }
        else if(bikeMode == "babbal"){
            modifyBabbalStatusForStandby();
            myGreeter.style.animation = "appearingGreeter 0.5s 1 ease-out normal forwards";
            greeter = "on";
            myLogoContainer.style.animation = "shrinkingLogo 0.5s 1 ease-in normal forwards"
            myLogo.style.animation = "shrinkingLogoActual 0.5s 1 ease-in normal forwards"
        }
        
        bikeMode="standby";
    }

    // Go to THIKKA mode
    else if(mode=="thikka"){
        if(bikeMode=="standby"){
            if(pos == 0){
                slideLeft();
            }

            if(greeter == "on"){
                myGreeter.style.animation = "vanishingGreeter 0.5s 1 ease-out normal forwards";
                greeter = "off";
            }

            if(keyboard =="closed"){
                myStatus.style.animation = "appearingIndicators 0.5s 1 ease-out normal forwards";
                myIndicators.style.animation = "appearingIndicatorsOpacity 0.5s 1 ease-out normal forwards";
                indicators = "on";
            }
            else if(keyboard == "open"){
                myIndicators.style.animation = "appearingIndicatorsOpacity 0.5s 1 ease-out normal forwards";
                indicators = "on";
            }
            mySpeed.style.animation = "appearingExtraStatus 1.5s 1 ease-out normal forwards";
            myPower.style.animation = "appearingExtraStatus 1.5s 1 ease-out normal forwards";
            // myRange.style.animation = "rangeSqueeze 0.5s 1 ease-out normal forwards";
            shrinkRange();
        }
        else if(bikeMode == "babbal"){
            babbalToThikka();
            // thikka();
        }
        bikeMode="thikka";
    }

    // Go to BABBAL mode
    else if(mode=="babbal"){
        // if(bikeMode == "standby"){
        //     standbyToBabbal();
        // }
        if(bikeMode == "thikka"){
                thikkaToBabbal();
        }
    }
}

function setGreeterState(state){
    if(state=="on" && greeter!="on"){
        myGreeter.style.animation = "appearingGreeter 0.5s 1 ease-out normal forwards";
        greeter = "on";
    }
    else if(state=="off" && greeter!="off"){
        myGreeter.style.animation = "vanishingGreeter 0.5s 1 ease-out normal forwards";
        greeter = "off";
    }
}

function modifyStandbyStatusForBabbal() {
    myStatus.style.animation = "appearingBabbalInfo 0.5s 1 ease-out normal forwards"
}

function modifyBabbalStatusForStandby() {
    myBabbalInfo.style.animation = "vanishingBabbalInfo 0.5s 1 ease-out normal forwards"
    myStatus.style.animation = "vanishingIndicators 0.5s 1 ease-out normal forwards"
}
// setMode("babbal");

function standbyToBabbal(){
    myMap.style.animation = "vanishingMap 0.5s 1 ease-out normal forwards";
    myHeartbeat.style.animation = "appearingHeartbeat 0.5s 1 ease-out normal forwards"
    myGreeter.style.animation = "vanishingGreeter 0.5s 1 ease-out normal forwards";
    myStatus.style.animation = "appearingIndicators 0.5s 1 ease-out normal forwards"
    myBabbalInfo.style.animation = "appearingBabbalInfo 0.5s 1 ease-out normal forwards";
    myLogoContainer.style.animation = "expandingLogo 0.5s 1 ease-out normal forwards";
    myLogo.style.animation = "expandingLogoActual 0.5s 1 ease-out normal forwards";
    greeter = "off";
    bikeMode="babbal"
}

function thikkaToBabbal(){
    if(keyboard == "open"){
        toggleKeyboard();
    }
    myMap.style.animation = "vanishingMap 0.5s 1 ease-out normal forwards";
    myHeartbeat.style.animation = "appearingHeartbeat 0.5s 1 ease-out normal forwards"
    myBabbalInfo.style.animation = "appearingBabbalInfo 0.5s 1 ease-out normal forwards";
    document.getElementById("info").style.animation = "vanishingInfo 0.5s 1 ease-out normal forwards";
    myLogo.style.animation = "expandingLogoActual 0.5s 1 ease-out normal forwards"
    bikeMode="babbal"
}

function babbalToThikka(){
    myMap.style.animation = "appearingMap 0.5s 1 ease-out normal forwards";
    myHeartbeat.style.animation = "vanishingHeartbeat 0.5s 1 ease-out normal forwards";
    myBabbalInfo.style.animation = "vanishingBabbalInfo 0.5s 1 ease-out normal forwards";
    document.getElementById("info").style.animation = "appearingInfo 0.5s 1 ease-out normal forwards";
    myLogo.style.animation = "shrinkingLogoActual 0.5s 1 ease-in normal forwards";
    // myStatus.style.animation = "appearingIndicators 0.5s 1 ease-out normal forwards";
    bikeMode="thikka";
}

function babbal(){
    document.getElementById("no-babbal").style.animation = "thikkaOff 0.5s 1 ease-out normal forwards";
    document.getElementById("babbal").style.animation = "babbalOn 0.5s 1 ease-out normal forwards";
}

function thikka(){
    document.getElementById("no-babbal").style.animation = "thikkaOn 0.5s 1 ease-out normal forwards";
    document.getElementById("babbal").style.animation = "babbalOff 0.5s 1 ease-out normal forwards";
}