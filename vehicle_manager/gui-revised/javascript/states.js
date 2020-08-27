function initKeyboardListener(){
    el = document.querySelector('input[type="text"]');
    document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].addEventListener('transitionstart', function(){
      let status=true;
      status = document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].classList.contains('mapboxgl-ctrl-geocoder--collapsed');
      
      if(status == true){
        if(previousMode != 'search-mode'){
            setMode(previousMode);
        }
      }
      else {
        setMode('search-mode');
      }
    });
  }

//  click handler for cancelling the navigation from nav-info-mode
document.getElementById('js-trip-cancel').addEventListener('click', function(){
    setMode('normal-mode');
});

//  click handler for starting the navigation from nav-info-mode
document.getElementById('js-start-navigation').addEventListener('click', function(){
    setMode('navigation-mode');
});

//  click handler for ending the navigation from navigation-mode
document.getElementById('js-end-navigation').addEventListener('click', function(){
    setMode('normal-mode');
});

// function to view or hide the trip info card
function setTripCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-trip-card').style.display = 'block';
    }
    else{
        document.getElementById('js-trip-card').style.display = 'none';
    }
}

// function to view or hide the dash card
function setDashCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-dash-card').style.display = 'block';
    }
    else{
        document.getElementById('js-dash-card').style.display = 'none';
    }
}

// function to view or hide the logo frame
function setLogoFrameVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-logo-frame').style.display = 'flex';
    }
    else{
        document.getElementById('js-logo-frame').style.display = 'none';
    }
}

// function to view or hide the banner-instructions card
function setRouteCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-route-card').style.display = 'block';
    }
    else{
        document.getElementById('js-route-card').style.display = 'none';
    }
}

// function to view or hide the geocoder
function setGeocoderVisibility(visibility){
    if(visibility == true){
        document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].style.display = 'block';
    }
    else{
        document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].style.display = 'none';
    }
}

// function to open or close the settings page
function setSettingsCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-settings-page').style.display = 'flex';
    }
    else {
        document.getElementById('js-settings-page').style.display = 'none';
    }
}

// function to open or close the settings page
function setNotificationCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-notification-card').style.display = 'block';
    }
    else {
        document.getElementById('js-notification-card').style.display = 'none';
    } 
}

// function to view or hide the software update notification
function setSWUpdateNotificationVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-swupdate-card').style.display = 'flex';
    }
    else {
        document.getElementById('js-swupdate-card').style.display = 'none';
    } 
}

function setBluetoothNotificationVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-bluetooth-card').style.display = 'flex';
    }
    else {
        document.getElementById('js-bluetooth-card').style.display = 'none';
    } 
}
function setKickstandSignalVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-kickstand-signal').style.display = 'flex';
    }
    else {
        document.getElementById('js-kickstand-signal').style.display = 'none';
    } 
}
function moveNotificationCard(to){
    if(to == 'navigation-mode'){
        document.getElementById('js-notification-card').style.top = '2.7vh';
    }
    else{
        document.getElementById('js-notification-card').style.top = '8.5vh';
    }
}
let previousMode = 'normal-mode';
let currentMode = 'normal-mode';
function setMode(mode){
    if(mode == currentMode){
        return;
    }
    switch(mode) {
        case 'normal-mode':
            setGeocoderVisibility(true);
            setRouteCardVisibility(false);
            setTripCardVisibility(false);
            setLogoFrameVisibility(true);
            setDashCardVisibility(true);
            moveNotificationCard(mode);
            closeKeyboard();
            previousMode = currentMode;
            currentMode = 'normal-mode';
            break;
        case 'search-mode':
            setDashCardVisibility(false);
            setTripCardVisibility(false);
            openKeyboard();
            previousMode = currentMode;
            currentMode = 'search-mode';
            break;
        case 'nav-info-mode':
            setLogoFrameVisibility(false);
            setRouteCardVisibility(false);
            setDashCardVisibility(true);
            setTripCardVisibility(true);
            closeKeyboard();
            previousMode = currentMode;
            currentMode = 'nav-info-mode';
            break;
        case 'navigation-mode':
            setTripCardVisibility(false);
            setRouteCardVisibility(true);
            setGeocoderVisibility(false);
            moveNotificationCard(mode);
            previousMode = currentMode;
            currentMode = 'navigation-mode';
            startNavigation();
            break;
        default:
            break;
    }
    console.log(previousMode + ' -> ' + currentMode);
}

// click handler for opening settings page
document.getElementById('js-dash-card').addEventListener('click', function(){
    setSettingsCardVisibility(true);
});

// click handler for closing the settings page
// click handler for informing user activity to backend
let settingsActiveArea = document.getElementById('js-settings-area');
let settingsPage = document.getElementById('js-settings-page');
document.addEventListener('click', function(event) {
    let isInsideActiveArea = settingsActiveArea.contains(event.target);
    let isInsidePage = settingsPage.contains(event.target);
    if (!isInsideActiveArea && isInsidePage) {
        setSettingsCardVisibility(false);
    }

    console.log('Page Active.')
    eel.updateUserActivityStatus(1);
});