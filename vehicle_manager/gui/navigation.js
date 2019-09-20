let bikeMode="standby";
let greeter = "on";
let indicators = "off";
let keyboard = "closed";
function toggleKeyboard(){
    if(bikeMode == "babbal"){
        return;
    }
    myStatus = document.getElementById("yatri-estate-2");
    myLogo = document.getElementById("yatri-logo-2");
    myGreeter = document.getElementById("greeter-1");
    myIndicators = document.getElementById("indicator");
    if(keyboard=='closed'){
        console.log("Opening Keyboard");
        if(myKeyboard != null){
            keyboard = 'open';

            if(bikeMode == "standby"){
                myLogo.style.boxShadow = "0px -4px 5px 0px rgba(219,219,219,1)";
                myStatus.style.animation ="vanishingStatusInStandby 0.5s 1 ease-out forwards";
                myStatus.addEventListener("animationend", logoShadowVanish);
            }
            else if(bikeMode == "thikka"){
                myLogo.style.boxShadow = "0px -4px 5px 0px rgba(219,219,219,1)";
                myStatus.style.animation ="vanishingStatus 0.5s 1 ease-out forwards";
                document.getElementById("status-2").style.animation = "vanishingStatusPadding 0.5s 1 ease-out forwards";
                myStatus.addEventListener("animationend", logoShadowVanish);
            }

            if(greeter == "on"){
                myGreeter.style.animation = "vanishingGreeter 0.5s 1 ease-out normal forwards";
                greeter = "off";
            }



        }
    }
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

            myStatus.style.display ="block";
            keyboard = 'closed';
            myLogo.style.boxShadow = "none";
        }
    }
}

function logoShadowVanish(){
    myLogo.style.boxShadow = "none";
}

function setMode(mode){
    if(mode == bikeMode){
        return;
    }
    myGreeter = document.getElementById("greeter-1");
    myStatus = document.getElementById("yatri-estate-2")
    myIndicators = document.getElementById("indicator");
    mySpeed = document.getElementById("speed");
    myPower = document.getElementById("power");
    myRange = document.getElementById("rangeMain");
    myMap = document.getElementById("map");
    myHeartbeat = document.getElementById("babbal-speed");
    myBabbalInfo = document.getElementById("babbal-info");
    myLogoContainer = document.getElementById("yatri-logo-2");
    myLogo = document.getElementById("yatri-logo-1");
    if(bikeMode=="babbal" && mode == "standby"){
        myMap.style.animation = "appearingMap 0.5s 1 ease-out normal forwards";
        myHeartbeat.style.animation = "vanishingHeartbeat 0.5s 1 ease-out normal forwards";
    }
    
    if(mode=="standby"){
        if(bikeMode=="thikka"){
            myRange.style.animation = "rangeEnlarge 0.5s 1 ease-out normal forwards";
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
        }
        else if(bikeMode == "babbal"){
            modifyBabbalStatusForStandby();
            myGreeter.style.animation = "appearingGreeter 0.5s 1 ease-out normal forwards";
            greeter = "on";
            myLogoContainer.style.animation = "shrinkingLogo 0.5s 1 ease-in normal forwards"
            myLogo.style.animation = "shrinkingLogoActual 0.5s 1 ease-in normal forwards"
        }
        else if(keyboard == "open"){
            //to-do
        }
        
        bikeMode="standby";
    }
    else if(mode=="thikka"){
        if(bikeMode=="standby"){


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
        myRange.style.animation = "rangeSqueeze 0.5s 1 ease-out normal forwards";
        }
        else if(bikeMode == "babbal"){
            babbalToThikka();
            // thikka();
        }
        bikeMode="thikka";
    }
    else if(mode=="babbal"){
        // if(bikeMode == "standby"){
        //     standbyToBabbal();
        // }
        if(bikeMode == "thikka"){
                thikkaToBabbal();
        }
        keyboard="closed"
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
    // myStatus.style.animation = "appearingIndicators 0.5s 1 ease-out normal forwards"
    myBabbalInfo.style.animation = "appearingBabbalInfo 0.5s 1 ease-out normal forwards";
    myLogoContainer.style.animation = "expandingLogo 0.5s 1 ease-out normal forwards"
    myLogo.style.animation = "expandingLogoActual 0.5s 1 ease-out normal forwards"
    greeter = "off";
    bikeMode="babbal"
}

function thikkaToBabbal(){
    // myMap.style.boxShadow = "0px 0px 15px -2px rgba(0,0,0,0.75)";
    myMap.style.animation = "vanishingMap 0.5s 1 ease-out normal forwards";
    myHeartbeat.style.animation = "appearingHeartbeat 0.5s 1 ease-out normal forwards"
    myBabbalInfo.style.animation = "appearingBabbalInfo 0.5s 1 ease-out normal forwards";
    myStatus.style.animation = "vanishingIndicators 0.5s 1 ease-out normal forwards";
    myLogoContainer.style.animation = "expandingLogo 0.5s 1 ease-out normal forwards"
    myLogo.style.animation = "expandingLogoActual 0.5s 1 ease-out normal forwards"
    bikeMode="babbal"
}

function babbalToThikka(){
    myMap.style.animation = "appearingMap 0.5s 1 ease-out normal forwards";
    myHeartbeat.style.animation = "vanishingHeartbeat 0.5s 1 ease-out normal forwards";
    myLogoContainer.style.animation = "shrinkingLogo 0.5s 1 ease-in normal forwards";
    myLogo.style.animation = "shrinkingLogoActual 0.5s 1 ease-in normal forwards";
    myBabbalInfo.style.animation = "vanishingBabbalInfo 0.5s 1 ease-out normal forwards";
    myStatus.style.animation = "appearingIndicators 0.5s 1 ease-out normal forwards";
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