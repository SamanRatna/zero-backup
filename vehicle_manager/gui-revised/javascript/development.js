// setSettingsCardVisibility(true);
// setNotificationCardVisibility(true);
// setSWUpdateNotificationVisibility(true);
// setBluetoothNotificationVisibility(true)

eel.expose(updateFinderRequest);
function updateFinderRequest(command){
    console.log('Finder Request: '+command);
    switch(command){
        case 'A':
            document.getElementById('js-finder-request').innerHTML = 'Flash Headlights';
            break;
        case 'B':
            document.getElementById('js-finder-request').innerHTML = 'Play Horn';
            break;
        case 'C':
            document.getElementById('js-finder-request').innerHTML = 'Play and Flash'
            break;
        default:
            return;
    }
    document.getElementById('js-finder-signal').style.display = 'flex';
    setTimeout(function(){
        document.getElementById('js-finder-signal').style.display = 'none';
    }, 5000);
}

document.getElementById('js-dash-card').style.display = 'none';