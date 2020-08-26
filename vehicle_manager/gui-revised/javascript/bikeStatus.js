// Function to update the speed and power in the dashboard
function updateSpeedPower(speed, power){
    document.getElementById('js-speed-value').innerHTML = speed;

    if(speed > 1){
        document.getElementById('js-trip-reset').classList.add('trip-reset-deactivated');
    }
    else{
        document.getElementById('js-trip-reset').classList.remove('trip-reset-deactivated');
    }
}

// Function to update the bike mode in the dashboard
let currentBikeMode = 'MODE_STANDBY'
let bikeModeStandby = document.getElementById('js-bikemode-standby');
let bikeModeSuste = document.getElementById('js-bikemode-suste');
let bikeModeThikka = document.getElementById('js-bikemode-thikka');
let bikeModeBabbal = document.getElementById('js-bikemode-babbal');
let bikeModeReverse = document.getElementById('js-bikemode-reverse');
let modeScroller = document.getElementById('js-mode-scroller');
function updateBikeMode(mode){
    switch(currentBikeMode){
        case 'MODE_STANDBY':
            bikeModeStandby.classList.toggle('mode-indicator-active');
            break;
        case 'MODE_SUSTE':
            bikeModeSuste.classList.toggle('mode-indicator-active');
            break;        
        case 'MODE_THIKKA':
            bikeModeThikka.classList.toggle('mode-indicator-active');
            break;
        case 'MODE_BABBAL':
            bikeModeBabbal.classList.toggle('mode-indicator-active');
            break;
        case 'MODE_REVERSE':
            bikeModeReverse.classList.toggle('mode-indicator-active');
            break;
    }
    switch(mode){
        case 'MODE_STANDBY':
            bikeModeStandby.classList.toggle('mode-indicator-active');
            modeScroller.style.marginTop = '-45px';
            break;
        case 'MODE_SUSTE':
            bikeModeSuste.classList.toggle('mode-indicator-active');
            modeScroller.style.marginTop = '-92px';
            break;        
        case 'MODE_THIKKA':
            bikeModeThikka.classList.toggle('mode-indicator-active');
            modeScroller.style.marginTop = '-138px';
            break;
        case 'MODE_BABBAL':
            bikeModeBabbal.classList.toggle('mode-indicator-active');
            modeScroller.style.marginTop = '-184px';
            break;
        case 'MODE_REVERSE':
            bikeModeReverse.classList.toggle('mode-indicator-active');
            modeScroller.style.marginTop = '0px';
            break;
    }
    currentBikeMode = mode;
}


// Function to update the battery level in the dashboard
let soc = document.getElementById('js-battery-value');
let batteryLevel = document.getElementById('js-battery-level');
let batteryCap = document.getElementById('js-battery-cap');
let range = document.getElementById('js-range');
function updateSOC(socData, suste, thikka, babbal){
    soc.innerHTML = socData + '%';
    batteryLevel.style.height = socData + '%';

    if(socData == 100){
        batteryCap.style.background = '#30D5C8';
    }
    else{
        batteryCap.style.background = 'rgba(48, 213, 200, 0.4)';
    }

    range.innerHTML = thikka;
}


// Function to update the odometer and trip distances
let odoDistance = document.getElementById('js-odo-distance');
let tripDistance = document.getElementById('js-trip-distance');
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
function updateTurnSignal(turnSignal){
    switch(turnSignal){
        case 0:
            rightTurnSignal.classList.remove('turn-signal-active');
            leftTurnSignal.classList.remove('turn-signal-active');
            break;
        case 1:
            rightTurnSignal.classList.add('turn-signal-active');
            leftTurnSignal.classList.remove('turn-signal-active');
            break;
        case 2:
            rightTurnSignal.classList.remove('turn-signal-active');
            leftTurnSignal.classList.add('turn-signal-active');
            break;
        case 3:
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
// Bluetooth
function requestBluetoothPairingConfirmation(passkey){
    document.getElementById('js-bluetooth-passkey').innerHTML = passkey;
    setBluetoothNotificationVisibility(true);
}

// accept bluetooth pairing
document.getElementById('js-ble-button-yes').addEventListener('click',function(){
    setBluetoothNotificationVisibility(true);
    respondBluetoothPairing('yes');  
});

// reject bluetooth pairing
document.getElementById('js-ble-button-no').addEventListener('click',function(){
    setBluetoothNotificationVisibility(false);
    respondBluetoothPairing('no');  
});

// bluetooth on-off toggle
document.getElementById('js-bluetooth-toggle').addEventListener('click', function(){
    document.getElementById('js-bluetooth-label-on').classList.toggle('active');
    document.getElementById('js-bluetooth-label-off').classList.toggle('active');
    document.getElementById('js-bluetooth-toggle-button').classList.toggle('toggled');
    
    if(document.getElementById('js-bluetooth-label-on').classList.contains('active')){
        eel.changeBluetoothState(true);
    }
    else{
        eel.changeBluetoothState(false);
    }
});

// update the name and status of th device connected to bluetooth
function updateBluetoothStatus(name, status){
    console.log("Bluetooth Status: " + name + " : " +status)
    if(status == '1'){
        document.getElementById('js-bluetooth-device').innerHTML = name;
    }
    else if(status == '0'){
        document.getElementById('js-bluetooth-device').innerHTML = ' ';
    }
}

function updateAdvertisementStatus(status){
    console.log("Bluetooth Advertisement Status: " + status)
    if(status =='1'){
        document.getElementById('js-bluetooth-label-on').classList.add('active');
        document.getElementById('js-bluetooth-label-off').classList.remove('active');
        document.getElementById('js-bluetooth-toggle-button').classList.add('toggled');
        document.getElementById('js-bluetooth-status').innerHTML = 'Discoverable';
    }
    else if(status == '0'){
        document.getElementById('js-bluetooth-label-on').classList.remove('active');
        document.getElementById('js-bluetooth-label-off').classList.add('active');
        document.getElementById('js-bluetooth-toggle-button').classList.remove('toggled');
        document.getElementById('js-bluetooth-status').innerHTML = 'Hidden';
    }
}
// Connectivity Settings
document.getElementById('js-settings-connectivity').addEventListener('click', function(){
    document.getElementById('js-settings-connectivity').classList.toggle('settings-connectivity-selected');
    document.getElementById('js-connectivity-pane').classList.toggle('right-pane-visible');
    document.getElementById('js-infographics-pane').classList.toggle('right-pane-visible');
});

function updateTime(){
    this.now = new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
    // console.log(this.now);
    document.getElementById('js-time').innerHTML = this.now;
    setTimeout(updateTime, 60000);
}
updateTime();