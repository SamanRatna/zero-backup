// toggle speed infograph unit km <-> mile
document.getElementById('js-speed-unit-toggle').addEventListener('click', function(){
    document.getElementById('js-speed-label-km').classList.toggle('active');
    document.getElementById('js-speed-label-mile').classList.toggle('active');
    document.getElementById('js-speed-unit-button').classList.toggle('toggled');
});

// toggle temperature infograph unit Celsius <-> Farenheit
document.getElementById('js-temperature-unit-toggle').addEventListener('click', function(){
    document.getElementById('js-temperature-label-c').classList.toggle('active');
    document.getElementById('js-temperature-label-f').classList.toggle('active');
    document.getElementById('js-temperature-unit-button').classList.toggle('toggled');
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

    if(status[0] =='2' || status[0] == '1'){
        document.getElementById('js-bluetooth-label-on').classList.add('active');
        document.getElementById('js-bluetooth-label-off').classList.remove('active');
        document.getElementById('js-bluetooth-toggle-button').classList.add('toggled');
        document.getElementById('js-bluetooth-status').innerHTML = 'Discoverable';
        document.getElementById('js-bluetooth-icon').style.backgroundImage = "url('icons/bluetooth-icon-discoverable.svg')";
    }
    else if(status[0] == '0'){
        document.getElementById('js-bluetooth-label-on').classList.remove('active');
        document.getElementById('js-bluetooth-label-off').classList.add('active');
        document.getElementById('js-bluetooth-toggle-button').classList.remove('toggled');
        document.getElementById('js-bluetooth-status').innerHTML = 'Hidden';
        document.getElementById('js-bluetooth-icon').style.backgroundImage = "url('icons/bluetooth-icon-off.svg')";
    }

    if(status.length > 1 ){
        document.getElementById('js-bluetooth-named-icon').innerHTML = status[1];
        document.getElementById('js-bluetooth-name').innerHTML = status[1];
    }
    toProcessing('js-bluetooth-toggle', false);
}

function updateBluetoothDevices(devices){
    // console.log(devices)
    for (index = 0; index < devices.length; index++) {
        let item = document.createElement('div');
        item.innerHTML = devices[index];
        item.classList.add('bluetooth-text')
        document.getElementById("js-bluetooth-content").appendChild(item);
    }
}

document.getElementById('js-bluetooth-name-edit').addEventListener('click', function(){
    console.log('Edit Bluetooth Name');
    openKeyboard('bluetooth');
    setBluetoothInputVisibility(true);
});

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
