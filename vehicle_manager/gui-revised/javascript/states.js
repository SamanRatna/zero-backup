function initKeyboardListener(){
    el = document.querySelector('input[type="text"]');
    document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].addEventListener('transitionend', function(){
      if(event.propertyName != 'width'){
          return;
      }
      let isCollapsed=true;
      isCollapsed = document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].classList.contains('mapboxgl-ctrl-geocoder--collapsed');
      
      if(isCollapsed == true){
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
    startNavigation(false);
    setMode('normal-mode');
});

//  click handler for starting the navigation from nav-info-mode
document.getElementById('js-start-navigation').addEventListener('click', function(){
    setMode('navigation-mode');
});

//  click handler for ending the navigation from navigation-mode
document.getElementById('js-end-navigation').addEventListener('click', function(){
    startNavigation(false);
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
    console.log('Setting Dash Card Visibility: ', visibility);
    if(visibility == true){
        document.getElementById('js-dash-card').style.display = 'flex';
        if(document.getElementsByClassName('mapboxgl-ctrl-logo')[0]){
            document.getElementsByClassName('mapboxgl-ctrl-logo')[0].style.transform = 'scale(3) translateX(30px) translateY(-80px)';
        }
    }
    else{
        document.getElementById('js-dash-card').style.display = 'none';
        if(document.getElementsByClassName('mapboxgl-ctrl-logo')[0]){
            document.getElementsByClassName('mapboxgl-ctrl-logo')[0].style.transform = 'scale(3) translateX(30px) translateY(-7px)';
        }
    }
}

// function to view or hide the logo frame
function setLogoFrameVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-logo-frame').style.display = 'flex';
        if(uiMode == 'map-mode'){
            document.getElementById('js-attribution-toggle').classList.remove('attribution-toggle-low');
        }
    }
    else{
        document.getElementById('js-logo-frame').style.display = 'none';
        if(uiMode == 'map-mode'){
            document.getElementById('js-attribution-toggle').classList.add('attribution-toggle-low');
        }
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
        if(document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0]){
            document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].style.display = 'block';
        }
    }
    else{
        if(document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0]){
            document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].style.display = 'none';
        }
    }
}

// function to open or close the settings page
function setSettingsCardVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-settings-page').style.display = 'flex';
        document.addEventListener('click', clickHandlerForSettingsPage);
        eel.onSettingsPage()
    }
    else {
        document.getElementById('js-settings-page').style.display = 'none';
        document.removeEventListener('click', clickHandlerForSettingsPage);
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

// function to view or hide the bluetooth pairing notification
function setBluetoothNotificationVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-bluetooth-card').style.display = 'flex';
    }
    else {
        document.getElementById('js-bluetooth-card').style.display = 'none';
    } 
}

function setBluetoothConnectionVisibililty(visibility){
    if(visibility == true){
        document.getElementById('js-ble-connection-notification').style.display = 'flex';
        setTimeout(function(){
            setBluetoothConnectionVisibililty(false);
        }, 5000);
    }
    else {
        document.getElementById('js-ble-connection-notification').style.display = 'none';
    }
}

// function to check the visibility of bluetooth pairing notification
function isBluetoothNotificationVisible(){
    if('none' == document.getElementById('js-bluetooth-card').style.display){
        return false;
    }
    else{
        return true;
    }
}
function setKickstandSignalVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-kickstand-signal').style.display = 'flex';
    }
    else {
        document.getElementById('js-kickstand-signal').style.display = 'none';
        document.getElementById('js-kickstand-signal').classList.remove('warning-pulse');
        pulseCounter = false;
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
            setDashCardOpacity(mode);
            closeKeyboard();
            // startNavigation(false);
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
            setDashCardOpacity(mode);
            previousMode = currentMode;
            currentMode = 'navigation-mode';
            startNavigation(true);
            break;
        case 'no-map-mode':
            setTripCardVisibility(false);
            setRouteCardVisibility(false);
            previousMode = currentMode;
            currentMode = 'no-map-mode';
            showInternetWarning(false);
            break;
        default:
            break;
    }
    console.log(previousMode + ' -> ' + currentMode);
}

// click handler for opening settings page
document.getElementById('js-dash-card-primary').addEventListener('click', function(){
    // setSettingsCardVisibility(true);
    switchUIMode();
});

document.getElementById('js-mode-indicator-no-map').addEventListener('click', function(){
    setSettingsCardVisibility(true);
});

// click handler for closing the settings page
// click handler for informing user activity to backend
let settingsActiveArea = document.getElementById('js-settings-area');
let settingsPage = document.getElementById('js-settings-page');


document.body.addEventListener('click', relayUserActivity);
function relayUserActivity(){
    console.log('Page Active.')
    eel.updateUserActivityStatus(1);
    return;
}
function clickHandlerForSettingsPage(event){
    // console.log('bluetoothInputActive: '+bluetoothInputActive)
    if(bluetoothInputActive){
        // console.log('bluetooth input is active.')
        return; 
    }
    let isInsideActiveArea = settingsActiveArea.contains(event.target);
    let isInsidePage = settingsPage.contains(event.target);
    // console.log('isInsideActiveArea: ' + isInsideActiveArea);
    // console.log('isInsidePage: ' + isInsidePage);
    if (!isInsideActiveArea && isInsidePage) {
        setSettingsCardVisibility(false);
    }
}

// function to change the opacity of the dash card based on the mode
function setDashCardOpacity(mode){
    if(mode == 'navigation-mode'){
        document.getElementById('js-dash-card').style.opacity = '0.5';
    }
    else{
        document.getElementById('js-dash-card').style.opacity = '1.0';
    }   
}

let bluetoothInputActive = false;
function setBluetoothInputVisibility(visibility){
    if(visibility == true){
        document.getElementById('js-bluetooth-input').style.display = 'block';
        bluetoothInputActive = true;
        document.removeEventListener('click', clickHandlerForSettingsPage);
    }
    else{
        document.getElementById('js-bluetooth-input').style.display = 'none';
        bluetoothInputActive = false;
        setTimeout(function(){
            document.addEventListener('click', clickHandlerForSettingsPage);
        }, 1000);
        
    }  
}

let signalBoxes = document.getElementsByClassName('signal-box');
let inputFields = document.getElementsByTagName('input');
function switchUITheme(){

    if(uiTheme == 'light'){
        uiTheme = 'dark';
        signalInactive = 'signal-box-dark';
        myKeyboard.setOptions({
            theme: "hg-theme-default hg-layout-default dark-theme"
          });
    }
    else{
        uiTheme = 'light';
        signalInactive = 'signal-box-light';
        myKeyboard.setOptions({
            theme: "hg-theme-default hg-layout-default"
        });
    }
    // document.getElementById('js-attribution-page').classList.toggle('dark');
    document.getElementById('js-theme-toggle').classList.toggle('dark');
    document.getElementById('js-dash-page').classList.toggle('dark');
    // updateBikeMode(currentBikeMode);
    document.getElementById('js-light-signal').classList.toggle('dark-signal');
    document.getElementById('js-settings-area').classList.toggle('dark');

    document.getElementsByClassName('settings-brightness-title')[0].classList.toggle('title-dark');
    document.getElementById('js-warning-content').classList.toggle('dark');
    document.getElementById('js-attribution-content').classList.toggle('dark');
    for(let i=0; i<signalBoxes.length; i++){
        if(!signalBoxes[i].classList.contains('turn-signal-active')){
            signalBoxes[i].classList.toggle('signal-box-light');
            signalBoxes[i].classList.toggle('signal-box-dark');
        }
    }

    document.getElementById('js-dash-card-primary').classList.toggle('dark');
    document.getElementById('js-dash-card-auxiliary').classList.toggle('dark');
    updateMapTheme();
    // if(isMapLoaded){
    //     switchMapMode(uiTheme);
    //     document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].classList.toggle('geocoder-dark');
    //     for(let i=0; i<inputFields.length; i++){
    //         inputFields[i].classList.toggle('geocoder-dark');
    //     }
    //     document.getElementsByClassName('suggestions')[0].classList.toggle('geocoder-dark');
    //     document.getElementsByClassName('mapboxgl-ctrl-compass')[0].parentElement.classList.toggle('geocoder-dark');

    //     document.getElementsByClassName('trip__info')[0].classList.toggle('dark');
    //     document.getElementsByClassName('route__info')[0].classList.toggle('dark');
    //     document.getElementsByClassName('route__info__current')[0].classList.toggle('dark');
    //     document.getElementsByClassName('route__summary')[0].classList.toggle('dark');
    // }
}

let mapTheme = 'light';
function updateMapTheme(){
    console.log('UI theme: '+uiTheme);
    console.log('Map theme: '+ mapTheme);
  if(mapTheme == uiTheme){
    return;
  }

  setMapStyleURI(uiTheme);
  if(isMapLoaded){
    switchMapMode(uiTheme);
    document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].classList.toggle('geocoder-dark');
    for(let i=0; i<inputFields.length; i++){
        inputFields[i].classList.toggle('geocoder-dark');
    }
    document.getElementsByClassName('suggestions')[0].classList.toggle('geocoder-dark');
    document.getElementsByClassName('mapboxgl-ctrl-compass')[0].parentElement.classList.toggle('geocoder-dark');

    document.getElementsByClassName('trip__info')[0].classList.toggle('dark');
    document.getElementsByClassName('route__info')[0].classList.toggle('dark');
    document.getElementsByClassName('route__info__current')[0].classList.toggle('dark');
    document.getElementsByClassName('route__summary')[0].classList.toggle('dark');
    mapTheme = uiTheme;
  }
}

let isRange = false;
function switchBatteryRange(){
    if(isRange){
        document.getElementById('js-range-value-box-no-map').style.display = 'none';
        document.getElementById('js-battery-value-box-no-map').style.display = 'flex';
        isRange = false;
    }else{
        document.getElementById('js-battery-value-box-no-map').style.display = 'none';
        document.getElementById('js-range-value-box-no-map').style.display = 'flex';
        isRange = true;
    }
}
document.getElementById('js-battery-indicator-no-map').addEventListener('click', function(){
    switchBatteryRange();
});
function setTouchDisabledIconVisibility(visibility){
    if(visibility){
        document.getElementById('js-touchdisable-icon').style.display = 'flex';
    } else {
        document.getElementById('js-touchdisable-icon').style.display = 'none';
    }
}
function setTouchDisabledNotificationVisibility(visibility){
    if(visibility){
        document.getElementById('js-touchdisable-signal').style.display = 'flex';
    } else {
        document.getElementById('js-touchdisable-signal').style.display = 'none';
    }
}
function setTouchDisabledWarningVisiblity(visibility){
    if(visibility){
        if(uiMode == 'no-map-mode'){
            setTouchDisabledNotificationVisibility(false);
            setTouchDisabledIconVisibility(true);
        } else if(uiMode == 'map-mode'){
            setTouchDisabledNotificationVisibility(true);
            setTouchDisabledIconVisibility(false);
        }
    } else {
        setTouchDisabledNotificationVisibility(false);
        setTouchDisabledIconVisibility(false);
    }
}

function disableTouch(value){
    if(value){
        document.body.style.pointerEvents = 'none';
        setTouchDisabledWarningVisiblity(true);
    }
    else{
        document.body.style.pointerEvents = 'auto';
        setTouchDisabledWarningVisiblity(false);
    }
}

// attribution page
document.getElementById('js-attribution-page').addEventListener('click', clickHandlerForAttributionPage);

let attributionActiveArea = document.getElementById('js-attribution-content');
function clickHandlerForAttributionPage(event){
  let isInsideActiveArea = attributionActiveArea.contains(event.target);
  if (!isInsideActiveArea) {
    document.getElementById('js-attribution-page').style.display = 'none';
  }
}

function setAttributionToggleVisibility(visibility){
    if(visibility){
        document.getElementById('js-attribution-toggle').style.display = 'flex';
    } else {
        document.getElementById('js-attribution-toggle').style.display = 'none';
    }
}

// warning page
document.getElementById('js-warning-page').addEventListener('click', clickHandlerForWarningPage);
function setWarningVisibility(visibility){
    if(visibility){
        document.getElementById('js-warning-page').style.display = 'flex';
    } else{
        stopWarningTimeout();
        document.getElementById('js-warning-page').style.display = 'none';
    }
}
let warningActiveArea = document.getElementById('js-warning-content');
function clickHandlerForWarningPage(event){
  let isInsideActiveArea = warningActiveArea.contains(event.target);
  if (!isInsideActiveArea) {
    setWarningVisibility(false);
  }
}
