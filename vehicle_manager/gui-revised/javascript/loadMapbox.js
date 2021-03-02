let isMapLoaded = false;
let isMapboxLoaded = false;

const mapboxScript_1 = document.createElement('script');
const mapboxScript_2 = document.createElement('script');
const mapboxScript_3 = document.createElement('script');
const mapboxScript_4 = document.createElement('script');

let isLoaded_Script1 = false;
let isLoaded_Script2 = false;
let isLoaded_Script3 = false;
let isLoaded_Script4 = false;

mapboxScript_1.src = 'https://api.mapbox.com/mapbox-gl-js/v1.8.1/mapbox-gl.js'
mapboxScript_1.id = 'mapboxScript_1'

mapboxScript_2.src = 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.2.0/mapbox-gl-geocoder.min.js'
mapboxScript_2.id = 'mapboxScript_2'

mapboxScript_3.src = 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v3.1.3/mapbox-gl-directions.js'
mapboxScript_3.id = 'mapboxScript_3'

mapboxScript_4.src = 'javascript/mapbox.js'
mapboxScript_4.id = 'mapboxScript_4'

mapboxScript_1.addEventListener('load', function() {
    isLoaded_Script1 = true;
    loadMapboxScript_2();
});

mapboxScript_2.addEventListener('load', function() {
    isLoaded_Script2 = true;
    loadMapboxScript_3();
});

mapboxScript_3.addEventListener('load', function() {
    isLoaded_Script3 = true;
    loadMapboxScript_4();
});

mapboxScript_4.addEventListener('load', function() {
    isLoaded_Script4 = true;
    startMap();
    updateUIMode('map-mode');
});


const mapboxLink_1 = document.createElement('link');
mapboxLink_1.rel = 'stylesheet';
mapboxLink_1.href = 'https://api.mapbox.com/mapbox-gl-js/v1.8.1/mapbox-gl.css';

const mapboxLink_2 = document.createElement('link');
mapboxLink_2.rel = 'stylesheet';
mapboxLink_2.href = 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.2.0/mapbox-gl-geocoder.css';

const mapboxLink_3 = document.createElement('link');
mapboxLink_3.rel = 'stylesheet';
mapboxLink_3.href = 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v3.1.3/mapbox-gl-directions.css';

const mapboxLink_4 = document.createElement('link');
mapboxLink_4.rel = 'stylesheet';
mapboxLink_4.href = 'css/mapbox.css';

function loadMapbox(){
    checkInternetConnectivity();
}

function onInternetConnectivity(status){
    // console.log(status, waitingForMapMode);
    if(status == true && waitingForMapMode==true){
        loadMapboxScript_1();
    } else if(status == false){
        waitingForMapMode = false;
        showInternetWarning(true, 'No internet Connectivity', true, true);
    }
}
function showInternetWarning(show, msg='', isTimeout=true, isWarning=false){
    if(show == false){
        document.getElementById('js-internet-signal').style.display = 'none';
        return;
    }

    document.getElementById('js-navigation-status-msg').innerHTML = msg;

    if(isWarning){
        document.getElementById('js-internet-signal').classList.add('signal-bar-warning');
    } else {
        document.getElementById('js-internet-signal').classList.remove('signal-bar-warning');
    }

    document.getElementById('js-internet-signal').style.display = 'flex';
    if(isTimeout){
        setTimeout(function(){
            document.getElementById('js-internet-signal').style.display = 'none';
        }, 5000);
    }
}
function loadMapboxScript_1(){
    showInternetWarning(true, 'Loading Map', false, false);
    if(!isLoaded_Script1){
        document.head.appendChild(mapboxLink_1);
        document.head.appendChild(mapboxScript_1);
    }
    else{
        loadMapboxScript_2();
    }
}
function loadMapboxScript_2(){
    if(!isLoaded_Script2){
        document.head.appendChild(mapboxLink_2);
        document.head.appendChild(mapboxScript_2);
    }
    else{
        loadMapboxScript_3();
    }
}
function loadMapboxScript_3(){
    if(!isLoaded_Script3){
        document.head.appendChild(mapboxLink_3);
        document.head.appendChild(mapboxScript_3);
    }
    else{
        loadMapboxScript_4();
    }
}
function loadMapboxScript_4(){
    if(!isLoaded_Script4){
        document.head.appendChild(mapboxLink_4);
        document.head.appendChild(mapboxScript_4);
        isMapboxLoaded = true;
    }
    else{
        startMap();
        updateUIMode('map-mode');
    }
}

function checkInternetConnectivity(){
    showInternetWarning(true, 'Checking internet Connectivity', false, false);
    eel.checkInternetConnectivity()
}

let mapStyleURI = 'mapbox://styles/yatri/cke13s7e50j3s19olk91crfkb?optimize=true';
let mapStyle = 'light';
function setMapStyleURI(style){
  mapStyle = style;
  if(style == 'light'){
    mapStyleURI = 'mapbox://styles/yatri/cke13s7e50j3s19olk91crfkb?optimize=true';
  }
  else if(style == 'dark'){
    mapStyleURI = 'mapbox://styles/yatri/ckgucl6jh0l9o19qj83mzbrjh?optimize=true';
  }
}

function onGPSStatus(status){
    if(status != 'READY'){
        showInternetWarning(true, 'GPS Signal not available', true, true);
    }
}
