let bikeMode="standby";
let greeter = "on";
let indicators = "off";
let keyboard = "closed";
function toggleKeyboard(){
    myStatus = document.getElementById("status-2");
    myLogo = document.getElementById("yatri-logo-2");
    myGreeter = document.getElementById("greeter-1");
    myIndicators = document.getElementById("indicator");
    if(keyboard=='closed'){
        console.log("Opening Keyboard");
        if(myKeyboard != null){
            keyboard = 'open';

            if(bikeMode == "standby"){
                myStatus.style.animation ="vanishingStatusInStandby 0.5s 1 ease-out forwards";
            }
            else if(bikeMode == "thikka"){
                myStatus.style.animation ="vanishingStatus 0.5s 1 ease-out forwards";
            }

            if(greeter == "on"){
                myGreeter.style.animation = "vanishingGreeter 0.5s 1 ease-out normal forwards";
                greeter = "off";
            }

            myLogo.style.boxShadow = "0px -4px 5px 0px rgba(219,219,219,1)";
        }
    }
    else if(keyboard =='open'){
        console.log("Closing Keyboard");
        if(myKeyboard != null){
            if(bikeMode == "thikka"){
                myStatus.style.animation ="appearingStatus 0.5s 1 ease-out forwards";
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


function setMode(mode){
    if(mode == bikeMode){
        return;
    }
    myGreeter = document.getElementById("greeter-1");
    myStatus = document.getElementById("status-2")
    myIndicators = document.getElementById("indicator");
    mySpeed = document.getElementById("speed");
    myPower = document.getElementById("power");
    myRange = document.getElementById("rangeMain");
    if(mode=="standby"){
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
            //to-do
        }
        mySpeed.style.animation = "vanishingExtraStatus 0.5s 1 ease-out normal forwards";
        myPower.style.animation = "vanishingExtraStatus 0.5s 1 ease-out normal forwards";
        myRange.style.animation = "rangeEnlarge 1s 1 ease-out normal forwards";
        bikeMode="standby";
    }
    else if(mode=="thikka"){
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
        mySpeed.style.animation = "appearingExtraStatus 0.5s 1 ease-out normal forwards";
        myPower.style.animation = "appearingExtraStatus 0.5s 1 ease-out normal forwards";
        myRange.style.animation = "rangeSqueeze 1s 1 ease-out normal forwards";
        bikeMode="thikka";


    }
}
