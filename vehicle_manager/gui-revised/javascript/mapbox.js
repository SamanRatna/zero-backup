let currentLocation = [];
let map;
let geocoder;
let destinationMarker, currentMarker;
const initialZoomLevel = 18;
const navigationZoomLevel = 20;
const navigationPitch = 0;
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
    // addStepMarkers(maneuvers); //this will add markers to the steps (debug functionality)
    findManeuverPoint(maneuvers);

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
          'line-width': 30,
          'line-opacity': 0.75
        }
      });
      map.getSource('route').setData(geojson);
    }

    // updateRouteToBackend(json.routes[0].geometry.coordinates)
    updateRouteToBackend(json.routes[0]);
  };
  req.send();
}

function addSummaryToPanel(route){
  let content = route.distance;
  let distance = Infinity;
  if(content > 999){
    distance = content / 1000;
    document.getElementById('js-trip-distance').innerHTML = distance.toFixed(1);
    document.getElementById('js-trip-distance-unit').innerHTML = 'km';
    document.getElementById('js-route-distance').innerHTML = distance.toFixed(1)+' km';
  }
  else{
    distance = content;
    document.getElementById('js-trip-distance').innerHTML = distance.toFixed(0);
    document.getElementById('js-trip-distance-unit').innerHTML = 'm';
    document.getElementById('js-route-distance').innerHTML = distance.toFixed(1)+' m';
  }
  document.getElementById('js-route-destination').innerHTML = 'To: '+ destinationName;

  setMode('nav-info-mode');
}

// function to find the closest maneuver point
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
  currentLeg = findClosestPoint(maneuver, closestManeuverIndex);
  closestManeuverIndex = currentLeg + 1;

  distanceToManeuver = calculateDistanceToManeuver(maneuvers[closestManeuverIndex]);
  distanceToDestination = calculateDistanceToDestination(distanceToManeuver, closestManeuverIndex, maneuver);
  let distanceToDestinationText = ' ';
  let distanceToManeuverText = ' ';
  if(distanceToDestination > 999){
    distanceToDestinationText = (distanceToDestination / 1000).toFixed(1)+' km';
  }
  else{
    distanceToDestinationText = (distanceToDestination).toFixed(0)+' m';
  }

  if(distanceToManeuver > 999){
    distanceToManeuverText = (distanceToManeuver / 1000).toFixed(1)+' km';
  }
  else{
    distanceToManeuverText = (distanceToManeuver).toFixed(0)+' m';
  }
  document.getElementById('js-route-distance').innerHTML = distanceToDestinationText;
  document.getElementById('js-distance-to-maneuver').innerHTML = ' ( ' + distanceToManeuverText + ' )';
  if(closestManeuverIndex != currentManeuverIndex){
    currentManeuverIndex = closestManeuverIndex;
    // console.log(closestManeuverPoint);
    document.getElementById('js-current-maneuver').innerHTML = maneuver[closestManeuverIndex].maneuver.instruction;
    let icon = findManeuverType('primary', maneuver[closestManeuverIndex].maneuver.type, maneuver[closestManeuverIndex].maneuver.modifier);
    document.getElementById('js-current-maneuver-icon').style.backgroundImage = icon;

    if(closestManeuverIndex + 1 < maneuver.length){
      setNextManeuverVisibility(true);
      document.getElementById('js-next-maneuver').innerHTML = maneuver[closestManeuverIndex+1].maneuver.instruction;
      let icon = findManeuverType('secondary', maneuver[closestManeuverIndex+1].maneuver.type, maneuver[closestManeuverIndex+1].maneuver.modifier);
      document.getElementById('js-next-maneuver-icon').style.backgroundImage = icon;
    }
    else{
      document.getElementById('js-next-maneuver').innerHTML = ' ';
      setNextManeuverVisibility(false);
    }

    // addRouteLeg(maneuver[currentLeg]); // this will show the current step on the map (debug functionality)
  }
  
}


const preIcon = "url('../icons/";
const postIcon = ".svg')";
const demarcator = '-';
function findManeuverType(step, type, modifier){
  let icon;
  if(type == 'depart' || type == 'arrive'){
    icon = preIcon + type + demarcator + step + postIcon;
  }
  else{
    icon = preIcon + 'turn' + demarcator + modifier + demarcator + step + postIcon;
  }
  return icon;
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
  eel.startNavigation();
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



function findClosestPoint(steps, closestStepIndex){
  let closestPointOne,
      closestPointTwo,
      closestPointIndexOne,
      closestPointIndexTwo,
      minDistanceOne = Infinity,
      minDistanceTwo = Infinity;
  let currentLeg;
  let closestIndex;

  let currentLngLat = mapboxgl.LngLat.convert(currentLocation);
  // calculate the closest maneuver
  steps[closestStepIndex].geometry.coordinates.forEach(function(point, pointIndex) {
    let currentPoint = mapboxgl.LngLat.convert(point);
    let currDistance = currentPoint.distanceTo(currentLngLat);
    if (currDistance < minDistanceOne) {
      minDistanceOne = currDistance;
      closestPointOne = point;
      closestPointIndexOne = pointIndex;
    }
  });

  if(closestStepIndex == 0){
    currentLeg = closestStepIndex;
    if(closestPointIndexOne == 0){
      currentLeg = currentLeg - 1;
    }
    return currentLeg;
  }
  steps[closestStepIndex-1].geometry.coordinates.forEach(function(point, pointIndex) {
    let currentPoint = mapboxgl.LngLat.convert(point);
    let currDistance = currentPoint.distanceTo(currentLngLat);
    if (currDistance < minDistanceTwo) {
      minDistanceTwo = currDistance;
      closestPointTwo = point;
      closestPointIndexTwo = pointIndex;
    }
  });


  if(minDistanceOne < minDistanceTwo){
    currentLeg =  closestStepIndex;
    closestIndex =closestPointIndexOne;
  }else{
    currentLeg =  (closestStepIndex - 1);
    closestIndex =closestPointIndexTwo;
  }

  if(closestIndex == 0){
    currentLeg = currentLeg - 1;
  }
  // console.log(closestStepIndex + ' : Leg Distance : ' + minDistanceOne);
  // console.log((closestStepIndex-1) + ' : Leg Distance : ' + minDistanceTwo);
  // console.log('Current Leg: ' + currentLeg);
  return currentLeg;
}

// function to calculate the distance to upcoming maneuver from the current location
function calculateDistanceToManeuver(upcomingStep){
  let currentLngLat = mapboxgl.LngLat.convert(currentLocation);
  let stepLngLat = mapboxgl.LngLat.convert(upcomingStep.maneuver.location);
  let distanceToManeuver = stepLngLat.distanceTo(currentLngLat);
  return distanceToManeuver;
}

// function to calculate the distance to destination from the current location
function calculateDistanceToDestination(distanceToManeuver, closestManeuverIndex, steps){
  let distanceToDestination = distanceToManeuver;
  for(index = closestManeuverIndex; index < steps.length; index++ ){
    distanceToDestination = distanceToDestination + steps[index].distance;
  }
  // console.log('Distance to Destination: ' + distanceToDestination)
  return distanceToDestination;
}

// Debug functionality
function addStepMarkers(steps){
  steps.forEach(function(step, stepIndex) {
    let marker = new mapboxgl.Marker()
    .setLngLat(step.maneuver.location)
    .addTo(map);
  });
}

function addRouteLeg(step){
  if(currentLeg < 0){
    return;
  }
  // console.log(step);
  let leg = step.geometry.coordinates;
    let geojson = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'LineString',
        coordinates: leg
      }
    };
    // if the route already exists on the map, reset it using setData
    if (map.getSource('leg')) {
      map.getSource('leg').setData(geojson);
    } else { // otherwise, make a new request
      map.addLayer({
        id: 'leg',
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
          'line-color': '#C4C4C4',
          'line-width': 20,
          'line-opacity': 1
        }
      });
      map.getSource('leg').setData(geojson);
    }
}