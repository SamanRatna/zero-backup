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

document.getElementById('js-trip-cancel').addEventListener('click', function(){
    setMode('normal-mode');
});

document.getElementById('js-start-navigation').addEventListener('click', function(){
    setMode('navigation-mode');
});

document.getElementById('js-end-navigation').addEventListener('click', function(){
    setMode('normal-mode');
});

function setTripCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-trip-card').style.display = 'block';
    }
    else{
        document.getElementById('js-trip-card').style.display = 'none';
    }
}

function setDashCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-dash-card').style.display = 'block';
    }
    else{
        document.getElementById('js-dash-card').style.display = 'none';
    }
}

function setLogoFrameVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-logo-frame').style.display = 'flex';
    }
    else{
        document.getElementById('js-logo-frame').style.display = 'none';
    }
}

function setRouteCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-route-card').style.display = 'block';
    }
    else{
        document.getElementById('js-route-card').style.display = 'none';
    }
}

function setGeocoderVisibility(visibility){
    if(visibility == true){
        document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].style.display = 'block';
    }
    else{
        document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].style.display = 'none';
    }
}

function setSettingsCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-settings-page').style.display = 'flex';
    }
    else {
        document.getElementById('js-settings-page').style.display = 'none';
    }
}

function setNotificationCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-notification-card').style.display = 'block';
    }
    else {
        document.getElementById('js-notification-card').style.display = 'none';
    } 
}

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
            previousMode = currentMode;
            currentMode = 'navigation-mode';
            startNavigation();
            break;
        default:
            break;
    }
    console.log(previousMode + ' -> ' + currentMode);
}