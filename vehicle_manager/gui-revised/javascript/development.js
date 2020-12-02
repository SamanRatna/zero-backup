// setSettingsCardVisibility(true);
// setNotificationCardVisibility(true);
// setSWUpdateNotificationVisibility(true);
// setBluetoothNotificationVisibility(true)

eel.expose(updateFinderRequest);
function updateFinderRequest(command){
    command = command.substring(1); //this removes the extra whitespace character in infront of the actual command character
                                    // for some reason this whitespace character is being received
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
            console.log('Finder Request not found.')
            return;
    }
    document.getElementById('js-finder-signal').style.display = 'flex';
    setTimeout(function(){
        document.getElementById('js-finder-signal').style.display = 'none';
    }, 5000);
}

// document.getElementById('js-dash-card').style.display = 'none';
document.getElementById('js-logo-frame').addEventListener('click', function(){
    location.reload();
});
