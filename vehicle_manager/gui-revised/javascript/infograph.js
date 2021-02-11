// toggle speed infograph unit km <-> mile
document.getElementById('js-speed-unit-toggle').addEventListener('click', function(){
    document.getElementById('js-speed-label-km').classList.toggle('active');
    document.getElementById('js-speed-label-mile').classList.toggle('active');
    document.getElementById('js-speed-unit-button').classList.toggle('toggled');
    if(document.getElementById('js-speed-label-mile').classList.contains('active')){
        changeUnitToMiles(true);
    } else {
        changeUnitToMiles(false);
    }
});

// toggle temperature infograph unit Celsius <-> Farenheit
document.getElementById('js-temperature-unit-toggle').addEventListener('click', function(){
    document.getElementById('js-temperature-label-c').classList.toggle('active');
    document.getElementById('js-temperature-label-f').classList.toggle('active');
    document.getElementById('js-temperature-unit-button').classList.toggle('toggled');
    if(document.getElementById('js-temperature-label-f').classList.contains('active')){
        changeUnitsToFarenheit(true);
    } else {
        changeUnitsToFarenheit(false);
    }
});

// brightness control slider
// let slider = document.getElementById('js-brightness-slider');
// slider.oninput = function() {
//     let x = slider.value * 10 - 5;
//     let color = 'linear-gradient(90deg, #30D5C8 ' + x + '%, #EAEAEA ' + x + '%)';
//     slider.style.background = color;
//     eel.changeBrightness(slider.value);
// }

// brightness control plus
document.getElementById('js-brightness-plus').addEventListener('click', function(){
    eel.changeBrightness(1);
});

//brightness control minus
document.getElementById('js-brightness-minus').addEventListener('click', function(){
    eel.changeBrightness(-1);
});

// Connectivity Settings
document.getElementById('js-settings-connectivity').addEventListener('click', function(){
    document.getElementById('js-settings-connectivity').classList.toggle('settings-connectivity-selected');
    document.getElementById('js-connectivity-pane').classList.toggle('right-pane-visible');
    document.getElementById('js-infographics-pane').classList.toggle('right-pane-visible');
});

// Bluetooth
function requestBluetoothPairingConfirmation(passkey){
    document.getElementById('js-bluetooth-passkey').innerHTML = passkey;
    setBluetoothNotificationVisibility(true);
    setTimeout(function(){
        if(isBluetoothNotificationVisible()){
            setBluetoothNotificationVisibility(false);
            respondBluetoothPairing('no');
        }
    }, 7000);
}

// accept bluetooth pairing
document.getElementById('js-ble-button-yes').addEventListener('click',function(){
    setBluetoothNotificationVisibility(false);
    respondBluetoothPairing('yes');  
});

// reject bluetooth pairing
document.getElementById('js-ble-button-no').addEventListener('click',function(){
    setBluetoothNotificationVisibility(false);
    respondBluetoothPairing('no');  
});

// bluetooth on-off toggle
document.getElementById('js-bluetooth-toggle').addEventListener('click', function(){
    toProcessing(this.id, true);
    // document.getElementById('js-bluetooth-label-on').classList.toggle('active');
    // document.getElementById('js-bluetooth-label-off').classList.toggle('active');
    // document.getElementById('js-bluetooth-toggle-button').classList.toggle('toggled');
    
    if(document.getElementById('js-bluetooth-label-on').classList.contains('active')){
        eel.changeBluetoothState(false);
    }
    else{
        eel.changeBluetoothState(true);
    }
});

// update the name and status of the device connected to bluetooth
function updateBluetoothStatus(name, status){
    console.log("Bluetooth Status: " + name + " : " +status)
    if(status == '1'){
        document.getElementById('js-bluetooth-device').innerHTML = name;
        document.getElementById('js-bluetooth-status').innerHTML = 'Connected';
        document.getElementById('js-ble-connected-device').innerHTML = 'Connected to '+ name;
        setBluetoothConnectionVisibililty(true);
    }
    else if(status == '0'){
        document.getElementById('js-bluetooth-device').innerHTML = ' ';
        document.getElementById('js-bluetooth-status').innerHTML = 'Discoverable';
        document.getElementById('js-ble-connected-device').innerHTML = 'Disconnected';
        setBluetoothConnectionVisibililty(true);
    }
}

function updateAdvertisementStatus(status){
    console.log("Bluetooth Advertisement Status: " + status)

    if(status=='ADVERTISEMENT_ON'){
        document.getElementById('js-bluetooth-label-on').classList.add('active');
        document.getElementById('js-bluetooth-label-off').classList.remove('active');
        document.getElementById('js-bluetooth-toggle-button').classList.add('toggled');
        document.getElementById('js-bluetooth-status').innerHTML = 'Discoverable';
        document.getElementById('js-bluetooth-icon').style.backgroundImage = "url('icons/bluetooth-icon-discoverable.svg')";
    }
    else if(status == 'ADVERTISEMENT_OFF'){
        document.getElementById('js-bluetooth-label-on').classList.remove('active');
        document.getElementById('js-bluetooth-label-off').classList.add('active');
        document.getElementById('js-bluetooth-toggle-button').classList.remove('toggled');
        document.getElementById('js-bluetooth-status').innerHTML = 'Hidden';
        document.getElementById('js-bluetooth-icon').style.backgroundImage = "url('icons/bluetooth-icon-off.svg')";
    }
    toProcessing('js-bluetooth-toggle', false);
}
function removeDevicesInUI(){
        // Remove the devices currently shown in the UI
        let devicesInUI = document.getElementsByClassName('bluetooth-paired-devices')
        for(index=devicesInUI.length; index > 0 ; index--){
            devicesInUI[0].parentNode.removeChild(devicesInUI[0]);
        }
}

function updateBluetoothDevices(devices){
    console.log(devices)

    // Remove the devices currently shown in the UI
    let devicesInUI = document.getElementsByClassName('bluetooth-paired-devices')
    for(index=devicesInUI.length; index > 0 ; index--){
        devicesInUI[0].parentNode.removeChild(devicesInUI[0]);
    }

    // Add the devices provided by the backend
    for (index = 0; index < devices.length; index++) {
        let item = document.createElement('div');
        item.innerHTML = devices[index];
        item.classList.add('bluetooth-text')
        item.classList.add('bluetooth-paired-devices')
        document.getElementById("js-bluetooth-content").appendChild(item);
    }
}

// document.getElementById('js-bluetooth-name-edit').addEventListener('click', function(){
//     console.log('Edit Bluetooth Name');
//     openKeyboard('bluetooth');
//     setBluetoothInputVisibility(true);
// });

function setBluetoothName(name){
    name = name.trim()
    if(name === ''){
        console.log('Cannot change name to an empty string.');
        return;
    }
    console.log('Setting Bluetooth Name to: ' + name)
    document.getElementById('js-bluetooth-name').innerHTML = name;
    // ask backend to change the bluetooth name
    eel.changeBluetoothName(name);
}

document.getElementById('js-bluetooth-name-edit-cancel').addEventListener('click', function(){
    closeKeyboard();
});
// function to update the network info
function updateNetworkInfo(info){
    console.log(info);
    if(info['simStatus'] == '1'){
        document.getElementById('js-network-icon').style.backgroundImage = "url('icons/network-icon-on-normal.svg')";
        document.getElementById('js-network-status').innerHTML = 'Enabled'

        document.getElementById('js-network-label-on').classList.add('active');
        document.getElementById('js-network-label-off').classList.remove('active');
        document.getElementById('js-network-toggle-button').classList.add('toggled');
    }
    else if(info['simStatus'] == '0'){
        document.getElementById('js-network-icon').style.backgroundImage = "url('icons/network-icon-off.svg')";
        document.getElementById('js-network-status').innerHTML = 'Disabled';
        document.getElementById('js-network-icon-name').innerHTML = ' ';
        document.getElementById('js-network-name').innerHTML = ' ';
    }
    if(info['networkName']){
        document.getElementById('js-network-icon-name').innerHTML = info['networkName'];
        document.getElementById('js-network-name').innerHTML = info['networkName'];
    }
    if(info['balance']){
        document.getElementById('js-network-balance').innerHTML = info['balance'];
    }
    if('gpsStatus' in info){
        // console.log('GPS Status: ' + info['gpsSatus'])
        let gpsStatus = info['gpsStatus'];
        if(gpsStatus == 'ON'){
            document.getElementById('js-gps-status').innerHTML = 'Enabled';
            isGPSActive = true;
            document.getElementById('js-gps-label-on').classList.add('active');
            document.getElementById('js-gps-label-off').classList.remove('active');
            document.getElementById('js-gps-toggle-button').classList.add('toggled');
        }
        else if(gpsStatus == 'OFF'){
            document.getElementById('js-gps-status').innerHTML = 'Disabled';
            isGPSActive = false;
            document.getElementById('js-gps-label-on').classList.remove('active');
            document.getElementById('js-gps-label-off').classList.add('active');
            document.getElementById('js-gps-toggle-button').classList.remove('toggled');
        }
        else if(gpsStatus == 'READY'){
            document.getElementById('js-gps-status').innerHTML = 'Enabled';
            isGPSActive = true;
            document.getElementById('js-gps-label-on').classList.add('active');
            document.getElementById('js-gps-label-off').classList.remove('active');
            document.getElementById('js-gps-toggle-button').classList.add('toggled');
            document.getElementById('js-gps-fix-status').innerHTML = 'Available'
        }
        toProcessing('js-gps-toggle', false);
    }

    if('internetConnectivity' in info){
        console.log('Internet Connectivity Checked.')
        let internetStatus = info['internetConnectivity'];
        onInternetConnectivity(internetStatus);
        if(internetStatus == true){
            document.getElementById('js-internet-status').innerHTML = 'Available';
        }
        else{
            document.getElementById('js-internet-status').innerHTML = 'Unavailable';
        }
    }
}

// network on-off toggle
// document.getElementById('js-network-toggle').addEventListener('click', function(){
//     document.getElementById('js-network-label-on').classList.toggle('active');
//     document.getElementById('js-network-label-off').classList.toggle('active');
//     document.getElementById('js-network-toggle-button').classList.toggle('toggled');
    
//     // if(document.getElementById('js-network-label-on').classList.contains('active')){
//     //     eel.changeNetworkState(true);
//     // }
//     // else{
//     //     eel.changeNetworkState(false);
//     // }
// });

function toProcessing(id, state){
    if(state == true){
        document.getElementById(id).classList.add('processing');
        document.getElementById(id+'-button').classList.add('processing');
    }
    if(state == false){
        document.getElementById(id).classList.remove('processing');
        document.getElementById(id+'-button').classList.remove('processing');
    }
}

let isGPSActive = false;
document.getElementById('js-gps-toggle').addEventListener('click', function(){
    toProcessing(this.id, true);
    console.log('isGPSActive: '+isGPSActive);
    if(isGPSActive){
        eel.setGPS(false);
    }
    else{
        eel.setGPS(true);
    }
});

function updateBluetoothName(name){
    document.getElementById('js-bluetooth-named-icon').innerHTML = name;
    document.getElementById('js-bluetooth-name').innerHTML = name;
}

// let navigationModeToggle = document.getElementById('js-navigation-mode-toggle');
// let navigationModeToggleState = 'no-map-mode';
// navigationModeToggle.addEventListener('click', switchUIMode);
// function updateNavigationToggle(mode){
//     console.log('updateNavigationToggle: '+mode);
//     navigationModeToggleState = mode;
//     if(mode == 'processing'){
//         navigationModeToggle.removeEventListener('click', switchUIMode);
//         navigationModeToggle.classList.remove('navigation-mode-active');
//         navigationModeToggle.classList.add('navigation-mode-processing');
//         setTimeout(function(){
//             if(navigationModeToggleState == 'processing'){
//                 updateNavigationToggle('no-map-mode');
//             }
//         }, 15000);
//     }
//     else if(mode == 'no-map-mode'){
//         navigationModeToggle.classList.remove('navigation-mode-processing')
//         navigationModeToggle.classList.remove('navigation-mode-active');
//         navigationModeToggle.addEventListener('click', switchUIMode);
//     }
//     else if(mode == 'map-mode'){
//         navigationModeToggle.classList.remove('navigation-mode-processing')
//         navigationModeToggle.classList.add('navigation-mode-active');
//         navigationModeToggle.addEventListener('click', switchUIMode);
//     }
// }

let themeToggle = document.getElementById('js-theme-toggle');
const themes = {
    LIGHT:  'light',
    DARK:   'dark',
    AUTO:   'auto'
}
let currentTheme = themes.LIGHT;
themeToggle.addEventListener('click', toggleUIMode);
function toggleUIMode(){
    switch(currentTheme){
        case themes.LIGHT:
            //switch to auto theme
            changeTheme(themes.AUTO);
            break;
        case themes.AUTO:
            //switch to dark theme
            changeTheme(themes.DARK);
            break;
        case themes.DARK:
            //switch to light theme
            changeTheme(themes.LIGHT);
            break;
    }
}

function changeTheme(toTheme){
    // check if toTheme is valid
    currentTheme = toTheme;
    switch(toTheme){
        case themes.LIGHT:
            document.getElementById('js-theme-name').innerHTML = 'Light <br /> Mode';
            if(uiTheme != 'light'){
                switchUITheme();
            }
            break;
        case themes.AUTO:
            document.getElementById('js-theme-name').innerHTML = 'Auto <br /> Mode';
            checkTimeForTheme();
            break;
        case themes.DARK:
            document.getElementById('js-theme-name').innerHTML = 'Dark <br /> Mode';
            if(uiTheme != 'dark'){
                switchUITheme();
            }
            break;
    }
}

function checkTimeForTheme(){
    if(currentTheme != themes.AUTO){
        return;
    }
    let date = new Date();
    let hour= date.getHours();
    if(hour > 7 && hour < 17){
        if(uiTheme != 'light'){
            switchUITheme();
        }
    }
    else{
        if(uiTheme != 'dark'){
            switchUITheme();
        }
    }
    setTimeout(checkTimeForTheme, 1800000);
}
