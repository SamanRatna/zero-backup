let currentLocation = [];
let map;
let geocoder;
let destinationMarker, currentMarker;
const initialZoomLevel = 16;
const navigationZoomLevel = 19;
/*
Request for API Key from the backend
*/
function startMap() {
  console.log('Executing getKeyFunction');
  eel.getAPIKey()(onAPIKeyResponse); // Must prefix call with 'await', otherwise it's the same syntax
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

  eel.getCurrentLocation()(onLocationResponse)
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

startMap();

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
    container: 'slide-map', // element where map is loaded
    style: 'mapbox://styles/yatri/ck7n2g8mw0mf41ipgdkwglthq',
    center: currentLocation, // starting position [lng, lat]
    zoom: initialZoomLevel
    });


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
  map.addControl(geocoder);
  
  // initialize the map canvas to interact with later
  var canvas = map.getCanvasContainer();

  // Current Location Marker
  currentMarker = new mapboxgl.Marker(elCurrentMarker) // initialize a new marker
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

    getRoute(currentLocation);
  });

  // Listen for the `result` event from the Geocoder
  // `result` event is triggered when a user makes a selection
  //  Add a marker at the result's coordinates
  geocoder.on('result', function(e) {
    // console.log(e);
    // console.log(e.place_name);
    addPlaceToPanel(e.result.place_name);
    map.getSource('single-point').setData(e.result.geometry);
    var coordsObj = e.result.geometry.coordinates;
    //   console.log(coordsObj);
    canvas.style.cursor = '';
  
    destinationMarker.setLngLat(coordsObj)
    .addTo(map);

    getRoute(coordsObj);
  });

  document.getElementById('start-navigation-button').addEventListener('click', function(){
    startNavigation();
  });

  document.getElementById('end-navigation-button').addEventListener('click', function(){
    endNavigation();
  });
  
  destinationMarker.on('dragend',onDragEnd);
  
  map.on('rotate', onRotate);
  
  document.getElementById('navigation-north').addEventListener('click', function(){
    map.resetNorth();
  });

  initKeyboardListener();
}
// create a function to make a directions request
function getRoute(end) {
  // make a directions request using cycling profile
  // an arbitrary start will always be the same
  // only the end or destination will change
  var start = [85.324, 27.717];
  var url = 'https://api.mapbox.com/directions/v5/mapbox/driving/' + start[0] + ',' + start[1] + ';' + end[0] + ',' + end[1] + '?steps=true&geometries=geojson&overview=full&access_token=' + mapboxgl.accessToken;

  // make an XHR request https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
  var req = new XMLHttpRequest();
  req.open('GET', url, true);
  req.onload = function() {
    var json = JSON.parse(req.response);
    var data = json.routes[0];
    console.log(json);
    addSummaryToPanel(data);
  //   addDirectionToPanel(data);
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
          'line-width': 10,
          'line-opacity': 0.75
        }
      });
    }
    // add turn instructions here at the end
    closeKeyboard();
  };
  req.send();
}

function addSummaryToPanel(route){
  let content = route.distance;
   let distance = content / 1000;
   document.getElementById('summary-distance').innerHTML = distance.toFixed(1) + 'km';
   document.getElementById('summary-box').style.display = 'block';
}
  
function addDirectionToPanel(route){
  let direction = route.legs[0].steps[0].maneuver[0];
  let directionBox = createElement('div');
  directionBox.setAttribute('id', 'direction-box');
  directionBox.innerHTML = direction;
}

function findManeuverPoint(maneuver){
  document.getElementById('navigation-button').style.display = 'none';
  document.getElementById('end-navigation-button').style.display = 'block';
  document.getElementById('maneuver-box').style.display = 'block';
  var closestManeuver,
  closestManeuverPoint,
  minDistance = Infinity;
  console.log("Current Location: " + currentLocation);
// calculate the closest maneuver
maneuver.forEach(function(man) {
  let currManeuverPoint = new H.geo.Point(
    man.position.latitude, 
    man.position.longitude
  );
  // console.log("Current Maneuver Point: " + currManeuverPoint);
  let currDistance = currManeuverPoint.distance(testLocation);
  console.log("Current Distance is: " + currDistance);
  if (currDistance < minDistance) {
    minDistance = currDistance;
    closestManeuver = man;
    closestManeuverPoint = currManeuverPoint;
  }
});
console.log(closestManeuverPoint);
console.log('closest maneuver (%s m) is at: {lat: %s, lng: %s}: \n %s', Math.round(minDistance), closestManeuverPoint.lat, closestManeuverPoint.lng, closestManeuver.instruction);
document.getElementById('maneuver-box').innerHTML = closestManeuver.instruction;
}

function addPlaceToPanel(place){
  let content = place;
   document.getElementById('summary-label').innerHTML = content;
   document.getElementById('summary-box').style.display = 'block';
}

function onDragEnd() {
  var lngLat = destinationMarker.getLngLat();
  let markerCoord = [lngLat.lng, lngLat.lat];
  console.log(markerCoord);
  getRoute(markerCoord);
}

function onRotate() {
  let bearing = -map.getBearing();
  // console.log(bearing);
  document.getElementById("navigation-north").style.transform = "rotate("+bearing+"deg)";
}

function startNavigation(){
  let cLngLat = currentMarker.getLngLat();
  let markerCoord = [cLngLat.lng, cLngLat.lat];
  map.flyTo({
    center: [
    cLngLat.lng,
    cLngLat.lat
    ],
    zoom: navigationZoomLevel,
    // essential: true // this animation is considered essential with respect to prefers-reduced-motion
    });
  document.getElementById('start-navigation-button').style.display = 'none';
  document.getElementById('end-navigation-button').style.display = 'block';
  document.getElementById('maneuver-box').style.display = 'block';
  document.getElementById('summary-box').style.display = 'block';

  // function to get the latitude and longitude of the vehicle and update it
}

function endNavigation(){
  document.getElementById('start-navigation-button').style.display = 'block';
  document.getElementById('end-navigation-button').style.display = 'none';
  document.getElementById('maneuver-box').style.display = 'none';
  document.getElementById('summary-box').style.display = 'none';
}
