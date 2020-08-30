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
    if(status[0] =='1'){
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
}

function updateBluetoothDevices(devices){
    // document.getElementById('js-bluetooth-passkey').innerHTML = devices[0];
    // setBluetoothNotificationVisibility(true);
    // setTimeout(function(){
    //     if(isBluetoothNotificationVisible()){
    //         setBluetoothNotificationVisibility(false);
    //     }
    // }, 7000);
    // logic to handle device lists
}

// function to update the network info
function updateNetworkInfo(info){
    console.log(info);
    if(info[0] == '1'){
        document.getElementById('js-network-icon').style.backgroundImage = "url('icons/network-icon-on-normal.svg')";
        document.getElementById('js-network-name').innerHTML = info[1];
    }
}