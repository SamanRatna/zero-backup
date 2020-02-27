/**
 * Moves the map to display over Berlin
 *
 * @param  {H.Map} map      A HERE Map instance within the application
 */
var currentLocation = '27.7279,85.3284';
// function moveMapToBerlin(map){
//     map.setCenter({lat:27.7279, lng:85.3284});
//     map.setZoom(18);
//   }
  
  let markers = [];
  /**
   * Boilerplate map initialization code starts below:
   */
  
  //Step 1: initialize communication with the platform
  var platform = new H.service.Platform({
    apikey: 'H3O5pr1qf71uc8XxXeeTYeA5bKAk5Bb3YLnzzlQb-w0',
    useHTTPS: true
  });
  // var defaultLayers = platform.createDefaultLayers({tileSize: 512,  
  //   ppi: 320 });
  var defaultLayers = platform.createDefaultLayers(512,  320 );
  
  //Step 2: initialize a map
  var map = new H.Map(document.getElementById('slide-map'),
    defaultLayers.vector.normal.map,{
    center: {lat:27.7279, lng:85.3284},
    zoom: 18,
    // pixelRatio: window.devicePixelRatio || 1
    pixelRatio: 1
  });
  // add a resize listener to make sure that the map occupies the whole container
  window.addEventListener('resize', () => map.getViewPort().resize());
  
  //Step 3: make the map interactive
  // MapEvents enables the event system
  // Behavior implements default interactions for pan/zoom (also on mobile touch environments)
  var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
  
  // Create the default UI components
  var ui = H.ui.UI.createDefault(map, defaultLayers);
  var geocoder = platform.getGeocodingService();
  var group = new H.map.Group();
  var mapSettings = ui.getControl('mapsettings');
  var zoom = ui.getControl('zoom');
  var scalebar = ui.getControl('scalebar');

  zoom.setVisibility(false);
  mapSettings.setVisibility(false);
  scalebar.setVisibility(false);
  
  var AUTOCOMPLETION_URL = 'https://autocomplete.geocoder.ls.hereapi.com/6.2/suggest.json',
  ajaxRequest = new XMLHttpRequest(),
  query = '';


/**
 * If the text in the text box  has changed, and is not empty,
 * send a geocoding auto-completion request to the server.
 *
 * @param {Object} textBox the textBox DOM object linked to this event
 * @param {Object} event the DOM event which fired this listener
 */
let suggestionsBox = document.getElementById('search-suggestions');
function autoCompleteListener(textBox, event) {

  if (query != textBox.value) {
    if(textBox.value.length == 0){
      clearOldSuggestions();
      suggestionsBox.style.display ='none';
    }
    else if (textBox.value.length >= 1) {

      /**
      * A full list of available request parameters can be found in the Geocoder Autocompletion
      * API documentation.
      *
      */
      var params = '?' +
        'query=' + encodeURIComponent(textBox.value) +   // The search text which is the basis of the query
        '&country=' + 'NPL' + //Limit results by country
        // '&beginHighlight=' + encodeURIComponent('<mark>') + //  Mark the beginning of the match in a token. 
        // '&endHighlight=' + encodeURIComponent('</mark>') + //  Mark the end of the match in a token. 
        '&maxresults=5' +  // The upper limit the for number of suggestions to be included 
        // in the response.  Default is set to 5.
        '&apiKey=' + 'H3O5pr1qf71uc8XxXeeTYeA5bKAk5Bb3YLnzzlQb-w0';
      ajaxRequest.open('GET', AUTOCOMPLETION_URL + params);
      ajaxRequest.send();
    }
  }
  query = textBox.value;
}

function autoCompleteListenerX(input) {

  if (query != input) {
    if(input.length == 0){
      clearOldSuggestions();
      // suggestionsBox.style.display ='none';
    }
    else if (input.length >= 1) {

      /**
      * A full list of available request parameters can be found in the Geocoder Autocompletion
      * API documentation.
      *
      */
      var params = '?' +
        'query=' + encodeURIComponent(input) +   // The search text which is the basis of the query
        '&country=' + 'NPL' + //Limit results by country
        // '&beginHighlight=' + encodeURIComponent('<mark>') + //  Mark the beginning of the match in a token. 
        // '&endHighlight=' + encodeURIComponent('</mark>') + //  Mark the end of the match in a token. 
        '&maxresults=5' +  // The upper limit the for number of suggestions to be included 
        // in the response.  Default is set to 5.
        '&apiKey=' + 'H3O5pr1qf71uc8XxXeeTYeA5bKAk5Bb3YLnzzlQb-w0';
      ajaxRequest.open('GET', AUTOCOMPLETION_URL + params);
      ajaxRequest.send();
    }
  }
  query = input;
}

/**
 *  This is the event listener which processes the XMLHttpRequest response returned from the server.
 */
function onAutoCompleteSuccess() {
  /*
   * The styling of the suggestions response on the map is entirely under the developer's control.
   * A representitive styling can be found the full JS + HTML code of this example
   * in the functions below:
   */
  clearOldSuggestions();
  addSuggestionsToPanel(this.response);  // In this context, 'this' means the XMLHttpRequest itself.
  // addSuggestionsToMap(this.response);
}


/**
 * This function will be called if a communication error occurs during the XMLHttpRequest
 */
function onAutoCompleteFailed() {
  alert('Ooops!');
}

// Attach the event listeners to the XMLHttpRequest object
ajaxRequest.addEventListener("load", onAutoCompleteSuccess);
ajaxRequest.addEventListener("error", onAutoCompleteFailed);
ajaxRequest.responseType = "json";

/**
 * The Geocoder Autocomplete API response retrieves a complete addresses and a `locationId`.
 * for each suggestion.
 *
 * You can subsequently use the Geocoder API to geocode the address based on the ID and 
 * thus obtain the geographic coordinates of the address.
 *
 * For demonstration purposes only, this function makes a geocoding request
 * for every `locationId` found in the array of suggestions and displays it on the map.
 * 
 * A more typical use-case would only make a single geocoding request - for example
 * when the user has selected a single suggestion from a list.
 *
 * @param {Object} response
 */

/**
 * Removes all H.map.Marker points from the map and adds closes the info bubble
 */
function clearOldSuggestions() {
  group.removeAll();
  // if (bubble) {
  //   bubble.close();
  // }
  // deleteTable();
  clearSuggestionsPanel();
}

function clearMarkers(){
  console.log(markers);
  while(markers.length){
    map.removeObject(markers.pop());
  }
}

/**
 * Format the geocoding autocompletion repsonse object's data for display
 *
 * @param {Object} response
 */
function addSuggestionsToPanel(response) {
  // console.log(JSON.stringify(response, null, ' '));
  var suggestions = document.getElementById('search-suggestions');
  suggestions.style.display = 'flex';
  // suggestions.innerHTML = JSON.stringify(response, null, ' ');
  // let geocodingParameters = {
  //   searchText: response.suggestions[0].label,
  //   jsonattributes: 1
  // };
  // geocode(geocodingParameters);

  // 
  // createTable();
  for(i in response.suggestions){
    // addRow(response.suggestions[i].label);
    addSuggestion(response.suggestions[i].label);
  }
}
// User location via browser's geolocation API
function updatePosition(event) {
  var coordinates = {
    lat: event.coords.latitude,
    lng: event.coords.longitude,
  };
  currentLocation = event.coords.latitude +','+event.coords.longitude;
  // Add a new marker every time the position changes
  var marker = new H.map.Marker(coordinates);
  marker.draggable = true;
  // map.addObject(marker);
  // markers.push(marker);
  // group.addObject(marker);
  // disable the default draggability of the underlying map
  // when starting to drag a marker object:
  // map.addEventListener('dragstart', function (ev) {
  //   var target = ev.target;
  //   if (target instanceof H.map.Marker) {
  //     behavior.disable();
  //   }
  // }, false);


  // re-enable the default draggability of the underlying map
  // when dragging has completed
  // map.addEventListener('dragend', function (ev) {
  //   var target = ev.target;
  //   if (target instanceof mapsjs.map.Marker) {
  //     behavior.enable();
  //   }
  // }, false);

  // Listen to the drag event and move the position of the marker
  // as necessary
  // map.addEventListener('drag', function (ev) {
  //   var target = ev.target,
  //     pointer = ev.currentPointer;
  //   if (target instanceof mapsjs.map.Marker) {
  //     target.setPosition(map.screenToGeo(pointer.viewportX, pointer.viewportY));
  //   }
  // }, false);
  // Recenter the map every time the position chnages
  map.setCenter(coordinates);
}

navigator.geolocation.watchPosition(updatePosition);


// Show suggestions in map
/**
 * Calculates and displays the address details of 200 S Mathilda Ave, Sunnyvale, CA
 * based on a free-form text
 *
 *
 * A full list of available request parameters can be found in the Geocoder API documentation.
 * see: http://developer.here.com/rest-apis/documentation/geocoder/topics/resource-geocode.html
 *
 * @param   {H.service.Platform} platform    A stub class to access HERE services
 */
function geocode(geocodingParameters) {
  // var geocoder = platform.getGeocodingService(),
  //   geocodingParameters = {
  //     searchText: '200 S Mathilda Sunnyvale CA',
  //     jsonattributes : 1
  //   };

  geocoder.geocode(
    geocodingParameters,
    onSuccess,
    onError
  );
}
/**
 * This function will be called once the Geocoder REST API provides a response
 * @param  {Object} result          A JSONP object representing the  location(s) found.
 *
 * see: http://developer.here.com/rest-apis/documentation/geocoder/topics/resource-type-response-geocode.html
 */
function onSuccess(result) {
  console.log(result);
  var locations = result.response.view[0].result;
  var loc = locations[0].location.displayPosition.latitude +','+locations[0].location.displayPosition.longitude;
  console.log(loc);
 /*
  * The styling of the geocoding response on the map is entirely under the developer's control.
  * A representitive styling can be found the full JS + HTML code of this example
  * in the functions below:
  */
  // addLocationsToMap(locations);
  clearMarkers();
  route(loc);
  // addLocationsToPanel(locations);
  // ... etc.
}

/**
 * This function will be called if a communication error occurs during the JSON-P request
 * @param  {Object} error  The error message received.
 */
function onError(error) {
  alert('Can\'t reach the remote server');
}
function addLocationsToMap(locations){
  var group = new  H.map.Group(),
    position,
    i;

  // Add a marker for each location found
  for (i = 0;  i < locations.length; i += 1) {
    position = {
      lat: locations[i].location.displayPosition.latitude,
      lng: locations[i].location.displayPosition.longitude
    };
    marker = new H.map.Marker(position);
    marker.label = locations[i].location.address.label;
    group.addObject(marker);
  }

  group.addEventListener('tap', function (evt) {
    map.setCenter(evt.target.getGeometry());
    openBubble(
       evt.target.getGeometry(), evt.target.label);
  }, false);

  // Add the locations group to the map
  map.addObject(group);
  map.setCenter(group.getBoundingBox().getCenter());
}

// Now use the map as required...
// geocode(platform);


// ---------------------------------------------------- Routing ----------------------------------- //
// Create the parameters for the routing request:
var routingParameters = {
  // The routing mode:
  'mode': 'fastest;car',
  // The start point of the route:
  'waypoint0': 'geo!50.1120423728813,8.68340740740811',
  // The end point of the route:
  'waypoint1': 'geo!52.5309916298853,13.3846220493377',
  // To retrieve the shape of the route we choose the route
  // representation mode 'display'
  'representation': 'display'
};

// Define a callback function to process the routing response:
var onResult = function(result) {
  console.log(result);
  var route,
    routeShape,
    startPoint,
    endPoint,
    linestring;
  if(result.response.route) {
  // Pick the first route from the response:
  route = result.response.route[0];

  addRouteShapeToMap(route);
  addSummaryToPanel(route);
  }
};

// Get an instance of the routing service:
var router = platform.getRoutingService();

function route(destination){
  var routingParameters = {
    // The routing mode:
    'mode': 'fastest;car',
    // The start point of the route:
    'waypoint0': currentLocation,
    // The end point of the route:
    'waypoint1': destination,
    // To retrieve the shape of the route we choose the route
    // representation mode 'display'
    'representation': 'navigation'
  };
  router.calculateRoute(routingParameters, onResult),
    function(error){
      alert(error.message);
    }
}


function addRouteShapeToMap(route){
  var lineString = new H.geo.LineString(),
    routeShape = route.shape,
    polyline;

  routeShape.forEach(function(point) {
    var parts = point.split(',');
    lineString.pushLatLngAlt(parts[0], parts[1]);
  });

  polyline = new H.map.Polyline(lineString, {
    style: {
      lineWidth: 4,
      strokeColor: 'rgba(0, 128, 255, 0.7)'
    }
  });

  // Retrieve the mapped positions of the requested waypoints:
  startPoint = route.waypoint[0].mappedPosition;
  endPoint = route.waypoint[1].mappedPosition;

  // Create a marker for the start point:
  var startMarker = new H.map.Marker({
    lat: startPoint.latitude,
    lng: startPoint.longitude
  });

  // Create a marker for the end point:
  var endMarker = new H.map.Marker({
    lat: endPoint.latitude,
    lng: endPoint.longitude
  });
  group.addObject(startMarker);
  group.addObject(endMarker);
  console.log(markers);
  markers.push(startMarker);
  markers.push(endMarker);
  // Add the polyline to the map
  map.addObjects([polyline, startMarker, endMarker]);
  // And zoom to its bounding rectangle
  map.getViewModel().setLookAtData({
    bounds: polyline.getBoundingBox()
  });
}


/**
 * Creates a series of H.map.Marker points from the route and adds them to the map.
 * @param {Object} route  A route as received from the H.service.RoutingService
 */
function addSummaryToPanel(route){
  let content = route.waypoint[1].label;
   document.getElementById('summary-label').innerHTML = content;
   document.getElementById('summary-box').style.display = 'block';
  
  let distance = route.leg[0].summary.distance / 1000;
  document.getElementById('summary-distance').innerHTML = distance.toFixed(1) + 'km';
}

function addDirectionToPanel(route){
  let direction = route.leg[0].maneuver[0].instruction;
  let directionBox = createElement('div');
  directionBox.setAttribute('id', 'direction-box');
  directionBox.innerHTML = direction;
}


Number.prototype.toMMSS = function () {
  return  Math.floor(this / 60)  +' minutes '+ (this % 60)  + ' seconds.';
}