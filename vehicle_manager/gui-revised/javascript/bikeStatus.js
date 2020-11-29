// function to update the variables based on map is activated or not
let soc = document.getElementById('js-battery-value-no-map');
let batteryLevel = document.getElementById('js-battery-level-no-map');
let batteryCap = document.getElementById('js-battery-cap-no-map');
let range = document.getElementById('js-range-no-map');
let speed = document.getElementById('js-speed-value-no-map');

let currentBikeMode = 'MODE_STANDBY'
let bikeModeStandby = document.getElementById('js-bikemode-standby-no-map');
let bikeModeSuste = document.getElementById('js-bikemode-suste-no-map');
let bikeModeThikka = document.getElementById('js-bikemode-thikka-no-map');
let bikeModeBabbal = document.getElementById('js-bikemode-babbal-no-map');
let bikeModeReverse = document.getElementById('js-bikemode-reverse-no-map');
let modeScroller = document.getElementById('js-mode-scroller-no-map');

let time = document.getElementById('js-time-no-map');

let noMapPage = document.getElementById('js-no-map-card');
let dashCard = document.getElementById('js-dash-card');

let uiMode = 'light';
function updateMapState(isMapLoaded){
    updateVariables(isMapLoaded);
    if(isMapLoaded){
        noMapPage.style.display = 'none';
        dashCard.style.display = 'flex';
    }
    else{
        noMapPage.style.display = 'flex';
        dashCard.style.display = 'none';
    }
}

function updateVariables(isMapLoaded){
    if(isMapLoaded){
        soc = document.getElementById('js-battery-value');
        batteryLevel = document.getElementById('js-battery-level');
        batteryCap = document.getElementById('js-battery-cap');
        range = document.getElementById('js-range');
        speed = document.getElementById('js-speed-value');
        time = document.getElementById('js-time');
        bikeModeSuste = document.getElementById('js-bikemode-suste');
        bikeModeThikka = document.getElementById('js-bikemode-thikka');
        bikeModeBabbal = document.getElementById('js-bikemode-babbal');
        bikeModeReverse = document.getElementById('js-bikemode-reverse');
        modeScroller = document.getElementById('js-mode-scroller');
        bikeModeStandby = document.getElementById('js-bikemode-standby');
    }
    else{
        soc = document.getElementById('js-battery-value-no-map');
        batteryLevel = document.getElementById('js-battery-level-no-map');
        batteryCap = document.getElementById('js-battery-cap-no-map');
        range = document.getElementById('js-range-no-map');
        speed = document.getElementById('js-speed-value-no-map');
        time = document.getElementById('js-time-no-map');
        bikeModeSuste = document.getElementById('js-bikemode-suste-no-map');
        bikeModeThikka = document.getElementById('js-bikemode-thikka-no-map');
        bikeModeBabbal = document.getElementById('js-bikemode-babbal-no-map');
        bikeModeReverse = document.getElementById('js-bikemode-reverse-no-map');
        modeScroller = document.getElementById('js-mode-scroller-no-map');
        bikeModeStandby = document.getElementById('js-bikemode-standby-no-map');
    }
}

// Function to update the speed and power in the dashboard
function updateSpeedPower(spd, power){
    console.log(spd, power);
    // console.log(spd);
    speed.innerHTML = Math.round(spd);

    if(spd > 1){
        activateTripResetButton(false);
    }
    else{
        activateTripResetButton(true);
    }
}

// Function to update the bike mode in the dashboard
let bikeModeActiveIndicator = 'mode-indicator-active';
function updateBikeMode(mode){
    console.log('Updating Bike Mode To: ' + mode)
    console.log(bikeModeActiveIndicator);
    // if(uiMode == 'light'){
    //     console.log('in light mode');
    //     switch(currentBikeMode){
    //         case 'MODE_STANDBY':
    //             bikeModeStandby.classList.toggle('mode-indicator-active');
    //             break;
    //         case 'MODE_SUSTE':
    //             bikeModeSuste.classList.toggle('mode-indicator-active');
    //             break;        
    //         case 'MODE_THIKKA':
    //             bikeModeThikka.classList.toggle('mode-indicator-active');
    //             break;
    //         case 'MODE_BABBAL':
    //             bikeModeBabbal.classList.toggle('mode-indicator-active');
    //             break;
    //         case 'MODE_REVERSE':
    //             bikeModeReverse.classList.toggle('mode-indicator-active');
    //             break;
    //     }
    // }
    // else{
    //     console.log('in dark mode');
    //     switch(currentBikeMode){
    //         case 'MODE_STANDBY':
    //             bikeModeStandby.classList.toggle('mode-indicator-active-dark');
    //             break;
    //         case 'MODE_SUSTE':
    //             bikeModeSuste.classList.toggle('mode-indicator-active-dark');
    //             break;        
    //         case 'MODE_THIKKA':
    //             bikeModeThikka.classList.toggle('mode-indicator-active-dark');
    //             break;
    //         case 'MODE_BABBAL':
    //             bikeModeBabbal.classList.toggle('mode-indicator-active-dark');
    //             break;
    //         case 'MODE_REVERSE':
    //             bikeModeReverse.classList.toggle('mode-indicator-active-dark');
    //             break;
    //     }
    // }
    
    // switch(mode){
    //     case 'MODE_STANDBY':
    //         bikeModeStandby.classList.toggle('mode-indicator-active');
    //         modeScroller.style.marginTop = '-45px';
    //         break;
    //     case 'MODE_SUSTE':
    //         bikeModeSuste.classList.toggle('mode-indicator-active');
    //         modeScroller.style.marginTop = '-92px';
    //         break;        
    //     case 'MODE_THIKKA':
    //         bikeModeThikka.classList.toggle('mode-indicator-active');
    //         modeScroller.style.marginTop = '-138px';
    //         break;
    //     case 'MODE_BABBAL':
    //         bikeModeBabbal.classList.toggle('mode-indicator-active');
    //         modeScroller.style.marginTop = '-184px';
    //         break;
    //     case 'MODE_REVERSE':
    //         bikeModeReverse.classList.toggle('mode-indicator-active');
    //         modeScroller.style.marginTop = '0px';
    //         break;
    // }
    switch(currentBikeMode){
        case 'MODE_STANDBY':
            bikeModeStandby.classList.toggle(bikeModeActiveIndicator);
            break;
        case 'MODE_SUSTE':
            bikeModeSuste.classList.toggle(bikeModeActiveIndicator);
            break;        
        case 'MODE_THIKKA':
            bikeModeThikka.classList.toggle(bikeModeActiveIndicator);
            break;
        case 'MODE_BABBAL':
            bikeModeBabbal.classList.toggle(bikeModeActiveIndicator);
            break;
        case 'MODE_REVERSE':
            bikeModeReverse.classList.toggle(bikeModeActiveIndicator);
            break;
    }
    switch(mode){
        case 'MODE_STANDBY':
            bikeModeStandby.classList.toggle(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-25%';
            break;
        case 'MODE_SUSTE':
            bikeModeSuste.classList.toggle(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-50%';
            break;        
        case 'MODE_THIKKA':
            bikeModeThikka.classList.toggle(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-80%';
            break;
        case 'MODE_BABBAL':
            bikeModeBabbal.classList.toggle(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-105%';
            break;
        case 'MODE_REVERSE':
            bikeModeReverse.classList.toggle(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '0%';
            break;
    }
    currentBikeMode = mode;
}


// Function to update the battery level in the dashboard
function updateSOC(socData, suste, thikka, babbal){
    if(socData > 100){
        return;
    }

    soc.innerHTML = socData + '%';
    batteryLevel.style.height = socData + '%';

    if(socData == 100){
        batteryCap.style.background = '#30D5C8';
    }
    else{
        batteryCap.style.background = 'rgba(48, 213, 200, 0.4)';
    }

    // range.innerHTML = thikka;
}

// Function to update the odometer and trip distances
let odoDistance = document.getElementById('js-odo-travel');
let tripDistance = document.getElementById('js-trip-travel');
function updateDistances(odo, trip){
    odoDistance.innerHTML = odo;
    tripDistance.innerHTML = trip;
}

// Function to update the turn signals
// turnSignal format (leftTurnSignalStatus, rightTurnSignalStatus)
let rightTurnSignal = document.getElementById('js-right-turn');
let leftTurnSignal = document.getElementById('js-left-turn');
let highBeamSignal = document.getElementById('js-high-beam');
let lowBeamSignal = document.getElementById('js-low-beam');
let signalInactive = 'signal-box-light';
function updateTurnSignal(turnSignal){
    switch(turnSignal){
        case 0:
            rightTurnSignal.classList.add(signalInactive);
            leftTurnSignal.classList.add(signalInactive);
            rightTurnSignal.classList.remove('turn-signal-active');
            leftTurnSignal.classList.remove('turn-signal-active');
            break;
        case 1:
            rightTurnSignal.classList.remove(signalInactive);
            leftTurnSignal.classList.add(signalInactive);
            rightTurnSignal.classList.add('turn-signal-active');
            leftTurnSignal.classList.remove('turn-signal-active');
            break;
        case 2:
            rightTurnSignal.classList.add(signalInactive);
            leftTurnSignal.classList.remove(signalInactive);
            rightTurnSignal.classList.remove('turn-signal-active');
            leftTurnSignal.classList.add('turn-signal-active');
            break;
        case 3:
            rightTurnSignal.classList.remove(signalInactive);
            leftTurnSignal.classList.remove(signalInactive);
            rightTurnSignal.classList.add('turn-signal-active');
            leftTurnSignal.classList.add('turn-signal-active');
            break;
    }
}
// Function to update the turn signals
// headlight signal format (lowBeamStatus, highBeamStatus)
function updateHeadlightSignal(headlightSignal){
    switch(headlightSignal){
        case 0:
            lowBeamSignal.classList.remove('low-beam-active');
            highBeamSignal.classList.remove('high-beam-active');
            break;
        case 1:
            lowBeamSignal.classList.remove('low-beam-active');
            highBeamSignal.classList.add('high-beam-active');
            break;
        case 2:
            lowBeamSignal.classList.add('low-beam-active');
            highBeamSignal.classList.remove('high-beam-active');
            break;
        case 3:
            lowBeamSignal.classList.add('low-beam-active');
            highBeamSignal.classList.add('high-beam-active');
            break;
    }
}

// Function to update the kick stand state
function updateStandState(standState){
    if(standState){
        setKickstandSignalVisibility(true);
    }
    else{
        setKickstandSignalVisibility(false);
    }
}

function updateTime(){
    this.now = new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
    // console.log(this.now);
    time.innerHTML = this.now;
    setTimeout(updateTime, 60000);
}
updateTime();

// function to activate or deactivate the trip reset button 
let tripResetState = true; // true means activated
function activateTripResetButton(activation){
    if(activation == true && tripResetState == false){
        document.getElementById('js-trip-reset').classList.remove('trip-reset-deactivated');
        document.addEventListener('click', requestTripReset);
        tripResetState = true;
    }
    else if(activation == false && tripResetState == true){
        document.getElementById('js-trip-reset').classList.add('trip-reset-deactivated');
        document.removeEventListener('click', requestTripReset);
        tripResetState = false;
    }
}

function requestTripReset(){
    eel.resetTrip();
}


function requestSWUpdateConfirmation(message){
    document.getElementById('js-swupdate-description').innerHTML = message;
    setSWUpdateNotificationVisibility(true);

}

document.getElementById('js-swupdate-install').addEventListener('click', function(){
    setSWUpdateNotificationVisibility(false);
    eel.swupdateResponse(true);
})

document.getElementById('js-swupdate-snooze').addEventListener('click', function(){
    setSWUpdateNotificationVisibility(false);
    eel.swupdateResponse(false);
})

function updateOrientation(heading, roll, pitch){
    console.log(heading, roll, pitch);
    updateHeadingTest(heading);
}
