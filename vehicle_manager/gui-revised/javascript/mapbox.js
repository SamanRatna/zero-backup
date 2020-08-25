let currentLocation = [];
let map;
let geocoder;
let destinationMarker, currentMarker;
const initialZoomLevel = 18;
const navigationZoomLevel = 24;
const navigationPitch = 60;
let maneuvers;
let destinationName;
let distanceToDestination = Infinity;
startMap();

/*
Request for API Key from the backend
*/
// function startMap() {
//   console.log('Executing getKeyFunction');
//   eel.getAPIKey()(onAPIKeyResponse);
// }

// dummy startMap function for UI development
function startMap() {
  console.log('Executing getKeyFunction');
  let key = "pk.eyJ1IjoieWF0cmkiLCJhIjoiY2swZzY1MDNqMDQ2ZzNubXo2emc4NHZwYiJ9.FtepvvGORqK03qJxFNvlEQ";
  onAPIKeyResponse(key)
}

/*
On receiving API Key from the backend
*/
function onAPIKeyResponse(key){
  if(key == null){
    console.log('Unable to retreive Mapbox API Key.')
    return;
  }

  mapboxgl.accessToken = key;
  console.log('Received Mapbox API Key');

  // eel.getCurrentLocation()(onLocationResponse) //uncomment this after removing dummy
  onLocationResponse([85.324, 27.717]) //dummy for UI development
}

/*
On receiving location from the backend
*/
function onLocationResponse(location){
  if(location == null){
    console.log('Unable to retreive current location.')
    return;
  }
  currentLocation = location;
  console.log("Current Location Received: " + currentLocation);
  initMap();
}

function initMap(){
  var elCurrentMarker = document.createElement('div');
  elCurrentMarker.className = 'current-marker';

  var elDestinationMarker = document.createElement('div');
  elDestinationMarker.className = 'destination-marker';

  destinationMarker = new mapboxgl.Marker({
    element: elDestinationMarker,
    draggable: true
  });

  // Initialize the map
  map = new mapboxgl.Map({
    container: 'js-map-card', // element where map is loaded
    // style: 'mapbox://styles/yatri/ck7n2g8mw0mf41ipgdkwglthq',
    style:'mapbox://styles/yatri/cke13s7e50j3s19olk91crfkb',
    center: currentLocation, // starting position [lng, lat]
    zoom: initialZoomLevel,
    // pitch: navigationPitch,
    attributionControl: false,
    keyboard: true,
    // antialias: true
    });

    map.addControl(new mapboxgl.AttributionControl({compact: false}), 'top-right');
  // Initialize a Geocoder
  geocoder = new MapboxGeocoder({ // Initialize the geocoder
      accessToken: mapboxgl.accessToken, // Set the access token
      // types: 'poi',
      countries: 'NP',
      collapsed: true,
      clearOnBlur: true,
      mapboxgl: mapboxgl, // Set the mapbox-gl instance
      marker: false, // Do not use the default marker style
  });
  
  // Add the geocoder to the map
  map.addControl(geocoder, 'top-left');
  
  // initialize the map canvas to interact with later
  var canvas = map.getCanvasContainer();

  // Current Location Marker
  currentMarker = new mapboxgl.Marker({
    element: elCurrentMarker,
    // pitchAlignment: viewport,
    draggable: true}) // initialize a new marker //elPsyCongroo
    .setLngLat(currentLocation) // Marker [lng, lat] coordinates
    .addTo(map); // Add the marker to the map

  addListeners();
}

function addListeners(){
  // After the map style has loaded on the page,
  // add a source layer and default styling for a single point
  map.on('load', function() {
    map.addSource('single-point', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: []
      }
    });
  });

  // Listen for the `result` event from the Geocoder
  // `result` event is triggered when a user makes a selection
  //  Add a marker at the result's coordinates
  geocoder.on('result', function(e) {
    geocoder.clear();
    document.getElementsByClassName('mapboxgl-ctrl-geocoder--input')[0].blur();
    // console.log(e);
    destinationName = e.result.text;
    // console.log(destinationName);
    // console.log(e.place_name);
    // addPlaceToPanel(e.result.place_name);
    map.getSource('single-point').setData(e.result.geometry);
    var coordsObj = e.result.geometry.coordinates;
    //   console.log(coordsObj);
    // canvas.style.cursor = '';
  
    destinationMarker.setLngLat(coordsObj)
    .addTo(map);

    getRoute(coordsObj);
  });

  // document.getElementById('start-navigation-button').addEventListener('click', function(){
  //   startNavigation();
  // });

  // document.getElementById('end-navigation-button').addEventListener('click', function(){
  //   endNavigation();
  // });
  

  map.on('rotate', onRotate);
  
  // document.getElementById('navigation-north').addEventListener('click', function(){
  //   map.resetNorth();
  // });

  initKeyboardListener();
}
// create a function to make a directions request
function getRoute(end) {
  closeKeyboard();
  closeSearchBox();
  // make a directions request using cycling profile
  // an arbitrary start will always be the same
  // only the end or destination will change
  var url = 'https://api.mapbox.com/directions/v5/mapbox/driving/' + currentLocation[0] + ',' + currentLocation[1] + ';' + end[0] + ',' + end[1] + '?steps=true&geometries=geojson&banner_instructions=true&overview=full&access_token=' + mapboxgl.accessToken;

  // make an XHR request https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
  var req = new XMLHttpRequest();
  req.open('GET', url, true);
  req.onload = function() {
    var json = JSON.parse(req.response);
    maneuvers = json.routes[0].legs[0].steps;
    var data = json.routes[0];
    console.log(json);
    addSummaryToPanel(data);
    // findManeuverPoint(maneuvers);
    // addMarkersToRoute(maneuvers);
    // elPsyCongroo
    currentMarker.on('dragend', function(){
      currentLocation = currentMarker.getLngLat();
      findManeuverPoint(maneuvers);
    });
    // elPsyCongroo
    var route = data.geometry.coordinates;
    var geojson = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'LineString',
        coordinates: route
      }
    };
    // if the route already exists on the map, reset it using setData
    if (map.getSource('route')) {
      map.getSource('route').setData(geojson);
    } else { // otherwise, make a new request
      map.addLayer({
        id: 'route',
        type: 'line',
        source: {
          type: 'geojson',
          data: {
            type: 'Feature',
            properties: {},
            geometry: {
              type: 'LineString',
              coordinates: geojson
            }
          }
        },
        layout: {
          'line-join': 'round',
          'line-cap': 'round'
        },
        paint: {
          'line-color': '#40e0d0',
          'line-width': 40,
          'line-opacity': 0.75
        }
      });
      map.getSource('route').setData(geojson);
    }
    // add turn instructions here at the end

    // updateRouteToBackend(json.routes[0].geometry.coordinates)
    updateRouteToBackend(json.routes[0]);
  };
  req.send();
}

function addSummaryToPanel(route){
  let content = route.distance;
  let distance = content / 1000;
  distanceToDestination = content;
  document.getElementById('js-trip-distance').innerHTML = distance.toFixed(1);
  document.getElementById('js-route-distance').innerHTML = distance.toFixed(1)+' km';
  document.getElementById('js-route-destination').innerHTML = 'To: '+ destinationName;

  setMode('nav-info-mode');
}

let currentManeuverIndex = -1;
function findManeuverPoint(maneuver){

  var closestManeuver,
  closestManeuverPoint,
  closestManeuverIndex,
  minDistance = Infinity;

  let currentLngLat = mapboxgl.LngLat.convert(currentLocation);
  // console.log("Current Location: " + currentLocation);
  // calculate the closest maneuver
  maneuver.forEach(function(man, manIndex) {
    let currManeuverPoint = mapboxgl.LngLat.convert(man.maneuver.location);
    // console.log("Current Maneuver Point: " + currManeuverPoint);
    let currDistance = currManeuverPoint.distanceTo(currentLngLat);
    // console.log("Current Distance is: " + currDistance);
    if (currDistance < minDistance) {
      minDistance = currDistance;
      closestManeuver = man;
      closestManeuverPoint = currManeuverPoint;
      closestManeuverIndex = manIndex;
    }
  });

  if(closestManeuverIndex != currentManeuverIndex){
    currentManeuverIndex = closestManeuverIndex;
    // console.log(closestManeuverPoint);
    // console.log('closest maneuver (%s m) is at: {lat: %s, lng: %s}: \n %s', Math.round(minDistance), closestManeuverPoint.lat, closestManeuverPoint.lng, closestManeuver.maneuver.instruction);
    document.getElementById('js-current-maneuver').innerHTML = closestManeuver.maneuver.instruction;

    if(closestManeuverIndex + 1 < maneuver.length){
      setNextManeuverVisibility(true);
      document.getElementById('js-next-maneuver').innerHTML = maneuver[closestManeuverIndex+1].maneuver.instruction;
    }
    else{
      document.getElementById('js-next-maneuver').innerHTML = ' ';
      setNextManeuverVisibility(false);
    }
    document.getElementById('js-current-maneuver-icon').style.backgroundImage = 'url(images/straight-ahead.svg)';
    document.getElementById('js-next-maneuver-icon').style.backgroundImage = 'url(images/turn-right.svg)';

    if(currentManeuverIndex > 0){
      distanceToDestination = Math.abs(distanceToDestination - maneuver[currentManeuverIndex-1].distance);
      document.getElementById('js-route-distance').innerHTML = distanceToDestination.toFixed(1)+' km';
    }
  }

}
// let currentManeuverIndex = -1;
// function findManeuverPoint(maneuver){

//   var closestManeuver,
//   closestManeuverPoint,
//   closestManeuverIndex,
//   minDistance = Infinity;

//   let currentLngLat = mapboxgl.LngLat.convert(currentLocation);
//   // console.log("Current Location: " + currentLocation);
//   // calculate the closest maneuver
//   let currDistance = Infinity;
//   maneuver.forEach(function(man, manIndex) {
//     let currManeuverPoint = mapboxgl.LngLat.convert(man.maneuver.location);
//     // console.log("Current Maneuver Point: " + currManeuverPoint);
//     currDistance = currManeuverPoint.distanceTo(currentLngLat);
//     console.log(manIndex + " Current Distance is: " + currDistance + ' : Leg Distance : ' + man.distance);
//     if (currDistance < minDistance) {
//       minDistance = currDistance;
//       closestManeuver = man;
//       closestManeuverPoint = currManeuverPoint;
//       closestManeuverIndex = manIndex;
//     }
//   });

//   //distance from
//   if(closestManeuverIndex < maneuver.length - 1){
//     nextManeuverPoint = mapboxgl.LngLat.convert(maneuver[closestManeuverIndex + 1].maneuver.location);
//     nextManeuverDistance = nextManeuverPoint.distanceTo(currentLngLat);
//     console.log('Current Leg Index: ' + closestManeuverIndex);
//     console.log('Current Leg Distance: ' + maneuver[closestManeuverIndex].distance);
//     console.log('Next Leg Distance: ' + maneuver[closestManeuverIndex + 1].distance );
//     console.log('Next Maneuver Distance: ' + nextManeuverDistance);
//     console.log('Current Maneuver Distance: ' + minDistance);
//     console.log('Instruction: ' + closestManeuver.maneuver.instruction);
//     console.log(' ');
//     if(nextManeuverDistance < 0.8 * maneuver[closestManeuverIndex].distance){
//       closestManeuver = maneuver[closestManeuverIndex + 1];
//       closestManeuverPoint = nextManeuverPoint;
//       closestManeuverIndex = closestManeuverIndex + 1;
//     }
//   }

//   if(closestManeuverIndex != currentManeuverIndex){
//     currentManeuverIndex = closestManeuverIndex;
//     // console.log(closestManeuverPoint);
//     // console.log('closest maneuver (%s m) is at: {lat: %s, lng: %s}: \n %s', Math.round(minDistance), closestManeuverPoint.lat, closestManeuverPoint.lng, closestManeuver.maneuver.instruction);
//     document.getElementById('js-current-maneuver').innerHTML = closestManeuver.maneuver.instruction;

//     if(closestManeuverIndex + 1 < maneuver.length){
//       setNextManeuverVisibility(true);
//       document.getElementById('js-next-maneuver').innerHTML = maneuver[closestManeuverIndex+1].maneuver.instruction;
//     }
//     else{
//       document.getElementById('js-next-maneuver').innerHTML = ' ';
//       setNextManeuverVisibility(false);
//     }
//     document.getElementById('js-current-maneuver-icon').style.backgroundImage = 'url(images/straight-ahead.svg)';
//     document.getElementById('js-next-maneuver-icon').style.backgroundImage = 'url(images/turn-right.svg)';

//     if(currentManeuverIndex > 0){
//       distanceToDestination = Math.abs(distanceToDestination - maneuver[currentManeuverIndex-1].distance);
//       document.getElementById('js-route-distance').innerHTML = distanceToDestination.toFixed(1)+' km';
//     }
//   }

// }


function onDragEnd() {
  var lngLat = destinationMarker.getLngLat();
  let markerCoord = [lngLat.lng, lngLat.lat];
  console.log(markerCoord);
  getRoute(markerCoord);
}

function onRotate() {
  let bearing = -map.getBearing();
  // console.log(bearing);
  // document.getElementById("navigation-north").style.transform = "rotate("+bearing+"deg)";
}

function startNavigation(){
  let cLngLat = currentMarker.getLngLat();
  let markerCoord = [cLngLat.lng, cLngLat.lat];
  map.easeTo({
    center: [ cLngLat.lng, cLngLat.lat ],
    pitch: navigationPitch,
    zoom: navigationZoomLevel,
    // essential: true // this animation is considered essential with respect to prefers-reduced-motion
    });

  // function to get the latitude and longitude of the vehicle and update it
  // eel.startNavigation();
}

function endNavigation(){
  document.getElementById('start-navigation-button').style.display = 'block';
  document.getElementById('end-navigation-button').style.display = 'none';
  document.getElementById('maneuver-box').style.display = 'none';
  document.getElementById('summary-box').style.display = 'none';
}

function closeSearchBox(){
  document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].classList.add('mapboxgl-ctrl-geocoder--collapsed');
}

function setNextManeuverVisibility(visibility) {
  if(visibility == true){
    document.getElementById('js-next-maneuver-box').style.display = 'flex';
    document.getElementById('js-maneuver-divider').style.display = 'flex';
  }
  else{
    document.getElementById('js-next-maneuver-box').style.display = 'none';
    document.getElementById('js-maneuver-divider').style.display = 'none';
  }
}

function addMarkersToRoute(data){

  data.forEach(function(man, manIndex) {
    man.maneuver.location 
    new mapboxgl.Popup()
    .setLngLat(man.maneuver.location)
    .setHTML(man.maneuver.instruction)
    .addTo(map);
  });
}

function updateBearing(data){
  currentLocation = [data[1], data[0]];
  bearing = -data[2];
  currentMarker.setLngLat(currentLocation);
  map.easeTo({
      center: currentLocation,
      bearing: bearing,
      speed: 0.01,
      maxDuration: 1900,
      essential: true
  });
  findManeuverPoint(maneuvers);
}