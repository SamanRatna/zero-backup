// function to update the variables based on map is activated or not
let soc = document.getElementById('js-battery-value-no-map');
let batteryLevel = document.getElementById('js-battery-level-no-map');
let batteryCap = document.getElementById('js-battery-cap-no-map');
let range = document.getElementById('js-range-value-no-map');
let speed = document.getElementById('js-speed-value-no-map');

let currentBikeMode = 'MODE_STANDBY'
let bikeModeStandby = document.getElementById('js-bikemode-standby-no-map');
let bikeModeSuste = document.getElementById('js-bikemode-suste-no-map');
let bikeModeThikka = document.getElementById('js-bikemode-thikka-no-map');
let bikeModeBabbal = document.getElementById('js-bikemode-babbal-no-map');
let bikeModeReverse = document.getElementById('js-bikemode-reverse-no-map');
let modeScroller = document.getElementById('js-mode-scroller-no-map');
let odoDistance = document.getElementById('js-odo-travel-no-map');
let tripDistance = document.getElementById('js-trip-travel-no-map');
let tripResetButton = document.getElementById('js-trip-reset-no-map');
let time = document.getElementById('js-time-no-map');

let noMapPage = document.getElementById('js-no-map-card');
let mapPage = document.getElementById('js-map-card');
let dashCard = document.getElementById('js-dash-card');

let uiTheme = 'light';
let uiMode = 'no-map-mode'

let lastMapUIMode = 'normal-mode'

// set this to true when switching from non-map mode to map-mode
// set this to false after switching to map-mode has completed
let waitingForMapMode = false;
function switchUIMode(){
    if(uiMode == 'no-map-mode'){
        waitingForMapMode = true;
        loadMapbox();
    }
    else if(uiMode == 'map-mode'){
        // if navigation is going on, cancel it
        if(currentMode == 'nav-info-mode' || currentMode == 'navigation-mode'){
            startNavigation(false);
            setMode('normal-mode');
        }
        updateUIMode('no-map-mode');
    }
}
function updateUIMode(mode){
    // console.log('Updating Map State: '+ true)

    uiMode = mode;
    resetBikeMode();
    updateVariables(mode);

    // sync data
    updateBikeMode(currentBikeMode);
    updateSOC(currentSOC, currentSOH, currentSusteRange, currentSusteRange, currentSusteRangevehicleReadings.carbonOffset);
    updateDistances(currentOdoReading, currentTripReading);
    updateTime();

    if(mode == 'map-mode'){
        waitingForMapMode = false;
        noMapPage.style.display = 'none';
        mapPage.style.display = 'flex';
        setDashCardVisibility(true);
        moveNotificationCard('normal-mode');
        setMode(lastMapUIMode);
    }
    else if(mode == 'no-map-mode'){
        noMapPage.style.display = 'flex';
        mapPage.style.display = 'none';
        setDashCardVisibility(false);
        moveNotificationCard('navigation-mode');
        lastMapUIMode = currentMode;
        setMode('no-map-mode');
    }
    updateNavigationToggle(mode);
}

function updateVariables(mode){
    if(mode == 'map-mode'){
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
        odoDistance = document.getElementById('js-odo-travel');
        tripDistance = document.getElementById('js-trip-travel');
        tripResetButton = document.getElementById('js-trip-reset');
    }
    else if(mode == 'no-map-mode'){
        soc = document.getElementById('js-battery-value-no-map');
        batteryLevel = document.getElementById('js-battery-level-no-map');
        batteryCap = document.getElementById('js-battery-cap-no-map');
        range = document.getElementById('js-range-value-no-map');
        speed = document.getElementById('js-speed-value-no-map');
        time = document.getElementById('js-time-no-map');
        bikeModeSuste = document.getElementById('js-bikemode-suste-no-map');
        bikeModeThikka = document.getElementById('js-bikemode-thikka-no-map');
        bikeModeBabbal = document.getElementById('js-bikemode-babbal-no-map');
        bikeModeReverse = document.getElementById('js-bikemode-reverse-no-map');
        modeScroller = document.getElementById('js-mode-scroller-no-map');
        bikeModeStandby = document.getElementById('js-bikemode-standby-no-map');
        odoDistance = document.getElementById('js-odo-travel-no-map');
        tripDistance = document.getElementById('js-trip-travel-no-map');
        tripResetButton = document.getElementById('js-trip-reset-no-map');
    }
}

// Function to update the speed and power in the dashboard
function updateSpeedPower(spd, power){
    // console.log(spd, power);

    speed.innerHTML = Math.round(spd);

    // if(spd > 1){
    //     activateTripResetButton(false);
    // }
    // else{
    //     activateTripResetButton(true);
    // }
}

// Function to update the bike mode in the dashboard
let bikeModeActiveIndicator = 'mode-indicator-active';
function resetBikeMode(){
    switch(currentBikeMode){
        case 'MODE_STANDBY':
            bikeModeStandby.classList.remove(bikeModeActiveIndicator);
            break;
        case 'MODE_SUSTE':
            bikeModeSuste.classList.remove(bikeModeActiveIndicator);
            break;
        case 'MODE_THIKKA':
            bikeModeThikka.classList.remove(bikeModeActiveIndicator);
            break;
        case 'MODE_BABBAL':
            bikeModeBabbal.classList.remove(bikeModeActiveIndicator);
            break;
        case 'MODE_REVERSE':
            bikeModeReverse.classList.remove(bikeModeActiveIndicator);
            break;
    }
}
function updateBikeMode(mode){
    console.log('Updating Bike Mode To: ' + mode)
    console.log(bikeModeActiveIndicator);
    // if(uiTheme == 'light'){
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
            bikeModeStandby.classList.remove(bikeModeActiveIndicator);
            break;
        case 'MODE_SUSTE':
            bikeModeSuste.classList.remove(bikeModeActiveIndicator);
            break;        
        case 'MODE_THIKKA':
            bikeModeThikka.classList.remove(bikeModeActiveIndicator);
            break;
        case 'MODE_BABBAL':
            bikeModeBabbal.classList.remove(bikeModeActiveIndicator);
            break;
        case 'MODE_REVERSE':
            bikeModeReverse.classList.remove(bikeModeActiveIndicator);
            break;
    }
    switch(mode){
        case 'MODE_REVERSE':
            // currentBikeMode = 'MODE_REVERSE'
            bikeModeReverse.classList.add(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '0%';
            break;
        case 'MODE_STANDBY':
            // currentBikeMode = 'MODE_STANDBY'
            bikeModeStandby.classList.add(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-25%';
            break;
        case 'MODE_SUSTE':
            // currentBikeMode = 'MODE_SUSTE'
            bikeModeSuste.classList.add(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-50%';
            break;        
        case 'MODE_THIKKA':
            // currentBikeMode = 'MODE_THIKKA'
            bikeModeThikka.classList.add(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-80%';
            break;
        case 'MODE_BABBAL':
            // currentBikeMode = 'MODE_BABBAL'
            bikeModeBabbal.classList.add(bikeModeActiveIndicator);
            modeScroller.style.marginTop = '-105%';
            break;
    }
    currentBikeMode = mode;
    if(currentBikeMode == 'MODE_STANDBY'){
        document.getElementById('js-p0-image-text').style.display = 'block'
        document.getElementById('js-p0-image').style.display = 'block'
        document.getElementById('js-stats-no-map').style.display = 'none'
    }else{
        document.getElementById('js-p0-image-text').style.display = 'none'
        document.getElementById('js-p0-image').style.display = 'none'
        document.getElementById('js-stats-no-map').style.display = 'block'
    }
}


// Function to update the battery level in the dashboard
let currentSOC = 0;
let currentSOH = 100;
let currentSusteRange = 0;
function updateSOC(socData, sohData, suste, thikka, babbal){
    // console.log('SOC received: '+socData + ' '+suste)
    if(socData > 100){
        return;
    }
    currentSOC = socData;
    currentSOH = sohData;
    soc.innerHTML = socData + '%';
    batteryLevel.style.height = socData + '%';

    if(socData == 100){
        batteryCap.style.background = '#30D5C8';
    }
    else{
        batteryCap.style.background = 'rgba(48, 213, 200, 0.4)';
    }
    if(suste){
        currentSusteRange = suste;
        if(uiMode == 'map-mode'){
            range.innerHTML = Math.round(suste);
        }
        else if(uiMode =='no-map-mode'){
            range.innerHTML = Math.round(suste) + 'km';
        }
    }
}

// Function to update the odometer and trip distances
let currentOdoReading = 0;
let currentTripReading = 0;
function updateDistances(odo, trip){
    currentOdoReading = odo;
    currentTripReading = trip;
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
        case 1:
            rightTurnSignal.classList.add(signalInactive);
            leftTurnSignal.classList.add(signalInactive);
            rightTurnSignal.classList.remove('turn-signal-active');
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
            leftTurnSignal.classList.add(signalInactive);
            rightTurnSignal.classList.add('turn-signal-active');
            leftTurnSignal.classList.remove('turn-signal-active');
            break;
        case 4:
            rightTurnSignal.classList.remove(signalInactive);
            leftTurnSignal.classList.remove(signalInactive);
            rightTurnSignal.classList.add('turn-signal-active');
            leftTurnSignal.classList.add('turn-signal-active');
            break;
    }
}
// Function to update the headlight signals
let lowbeamState = false;
let highbeamState = false;
let headlightState = 1;
function updateHeadlightSignal(light, signal){
    console.log('Head Light State: '+signal);
    if(light == 1){ // low beam
        if(signal == 1){ // off
            lowbeamState = false;
        }
        else if(signal == 2){ // on
            lowbeamState = true;
        }
    }
    else if(light == 2){ // high beam
        if(signal == 1){ // off
            highbeamState = false;
        }
        else if(signal == 2){ // on
            highbeamState = true;
        }
    }

    if(highbeamState){
        headlightState = 3;
    }
    else if(lowbeamState){
        headlightState = 2;
    }
    else{
        headlightState = 1;
    }
    switch(headlightState){
        case 1:
            lowBeamSignal.classList.add(signalInactive);
            highBeamSignal.classList.add(signalInactive);
            lowBeamSignal.classList.remove('low-beam-active');
            highBeamSignal.classList.remove('high-beam-active');
            break;
        case 2:
            lowBeamSignal.classList.remove(signalInactive);
            highBeamSignal.classList.add(signalInactive);
            lowBeamSignal.classList.add('low-beam-active');
            highBeamSignal.classList.remove('high-beam-active');
            break;
        case 3:
            lowBeamSignal.classList.add(signalInactive);
            highBeamSignal.classList.remove(signalInactive);
            lowBeamSignal.classList.remove('low-beam-active');
            highBeamSignal.classList.add('high-beam-active');
            break;
    }
}

// Function to update the kick stand state
function updateStandState(standState){
    if(standState == 1){
        setKickstandSignalVisibility(true);
    }
    else if(standState == 2){
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
let tripResetState = false; // true means activated
activateTripResetButton(true);
function activateTripResetButton(activation){
    if(activation == tripResetState){
        // console.log('Trip Reset Button already in the requested state: ', activation)
    }
    else if(activation == true && tripResetState == false){
        console.log('Activating Trip Reset Button.')
        document.getElementById('js-trip-reset').classList.remove('trip-reset-deactivated');
        document.getElementById('js-trip-reset').addEventListener('click', requestTripReset);
        document.getElementById('js-trip-reset-no-map').classList.remove('trip-reset-deactivated');
        document.getElementById('js-trip-reset-no-map').addEventListener('click', requestTripReset);
        tripResetState = true;
    }
    else if(activation == false && tripResetState == true){
        console.log('Deactivating Trip Reset Button.')
        document.getElementById('js-trip-reset').classList.add('trip-reset-deactivated');
        document.getElementById('js-trip-reset').removeEventListener('click', requestTripReset);
        document.getElementById('js-trip-reset-no-map').classList.add('trip-reset-deactivated');
        document.getElementById('js-trip-reset-no-map').removeEventListener('click', requestTripReset);
        tripResetState = false;
    }
}

function requestTripReset(){
    console.log('Requesting trip reset')
    eel.resetTripData();
}


// function requestSWUpdateConfirmation(message){
//     document.getElementById('js-swupdate-description').innerHTML = message;
//     setSWUpdateNotificationVisibility(true);

// }

// document.getElementById('js-swupdate-install').addEventListener('click', function(){
//     setSWUpdateNotificationVisibility(false);
//     eel.swupdateResponse(true);
// })

// document.getElementById('js-swupdate-snooze').addEventListener('click', function(){
//     setSWUpdateNotificationVisibility(false);
//     eel.swupdateResponse(false);
// })

function updateOrientation(heading, roll, pitch){
    // console.log(heading, roll, pitch);
    // console.log('Heading: '+heading)
    if(uiMode == 'no-map-mode'){ //go to map mode
        if(pitch > 10 || pitch < -10){
            document.getElementById('js-pitch-indicator').classList.add('pitch-dial-caution');
        }
        else{
            document.getElementById('js-pitch-indicator').classList.remove('pitch-dial-caution');
        }
        pitch = pitch > 10 ? 10 : pitch < -10 ? -10 : pitch;
        scaledPitch = pitch / 10 * 115;
    
        document.getElementById('js-roll-indicator').style.transform = 'rotate('+roll+'deg)';
        document.getElementById('js-pitch-indicator').style.transform = 'translate(0px,'+ scaledPitch + 'px)';
        document.getElementById('js-yaw-indicator').style.transform = 'rotate('+ heading + 'deg)';
    }
    else if(uiMode == 'map-mode'){ // go to no-map-mode
        updateHeading(heading)
    }

    // updateHeading(heading)
    // if(pitch > 10 || pitch < -10){
    //     document.getElementById('js-pitch-indicator').classList.add('pitch-dial-caution');
    // }
    // else{
    //     document.getElementById('js-pitch-indicator').classList.remove('pitch-dial-caution');
    // }
    // pitch = pitch > 10 ? 10 : pitch < -10 ? -10 : pitch;
    // scaledPitch = pitch / 10 * 115;

    // document.getElementById('js-roll-indicator').style.transform = 'rotate('+roll+'deg)';
    // document.getElementById('js-pitch-indicator').style.transform = 'translate(0px,'+ scaledPitch + 'px)';
    // document.getElementById('js-yaw-indicator').style.transform = 'rotate('+ heading + 'deg)';
    // updateHeadingTest(heading);
}

eel.expose(updateRiderInfo);
function updateRiderInfo(info){
    if("Name" in info){
        document.getElementById('js-account-person').innerHTML = info["Name"];
    }
    if("LicenseNumber" in info){
        document.getElementById('js-account-license').innerHTML = 'Lic. # ' + info["LicenseNumber"];
    }
    if("BikeNumber" in info){
        document.getElementById('js-account-vehicle').innerHTML = info["BikeNumber"];
    }
}

eel.expose(updateTripMaxSpeed);
function updateTripMaxSpeed(speed){
    document.getElementById('js-trip-max-speed').innerHTML = speed;
}


// rider info
let count = 0;
let elements = new Map();
document.getElementById('js-rider-info').addEventListener('click', function (event) {
  let countdown;
  function reset () {
    count = 0;
    countdown = null;
  }
  count++;
  if (count === 5) {
    if (!elements.has(event.target)) {
      elements.set(event.target, 1);
    } else {
      let currentCount = elements.get(event.target);
      currentCount++;
      elements.set(event.target, currentCount);
    }
    let fiveClick = new CustomEvent('fiveClicks', {
      bubbles: true,
      detail: {
        numberOfFiveClicks: elements.get(event.target)
      }
    });
    event.target.dispatchEvent(fiveClick);
    reset();
  }
  if (!countdown) {
    countdown = window.setTimeout(function () {
      reset();
    }, 1500);
  }
});
document.getElementById('js-rider-info').addEventListener('fiveClicks', function (event) {
    eel.fetchRiderInfo();
    console.log('This element has been five-clicked', event.detail.numberOfFiveClicks, 'times');
});

eel.expose(updateBikeOnOffStatus);
function updateBikeOnOffStatus(state){
    if(state == true){  // if bike is turning ON
        document.body.style.pointerEvents = 'auto';
    }else{  // if bike is turning OFF
        document.body.style.pointerEvents = 'none';
    }
}
