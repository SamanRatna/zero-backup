var map;
var directionsDisplay;
let currentPosition;
var directionsService;
var directionsRenderer;
let navigateButton = document.getElementById("navigation-button");
let searchField = document.getElementById('autocomplete');
function initMap() {
    let mapLocation = {lat: 27.7279, lng: 85.3284};
    map = new google.maps.Map(document.getElementById('slide-map'), {
        center: mapLocation,
        disableDefaultUI: true,
        scaleControl: true,
        zoom: 13,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        // styles: darkStyle
        styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
    });
    
    // The marker, positioned at kathmandu
    var marker = new google.maps.Marker({position: mapLocation, map: map});

    var request = {
        // origin: new google.maps.LatLng(27.7279, 85.3284),
        // destination: new google.maps.LatLng(28.570317, 77.321820),
        origin: {lat: 27.7279, lng: 85.3284},
        destination: {lat: 27.7213, lng: 85.3149},
        travelMode: google.maps.DirectionsTravelMode.DRIVING
     }
     var directionsService = new google.maps.DirectionsService();
     directionsService.route(request, function(response, status) {
           if (status === google.maps.DirectionsStatus.OK) {
            new google.maps.DirectionsRenderer({
                map: map,
                directions: response
              });
               // For each route, display summary information.
           } else {
               console.log('Directions request failed due to ' + status, response);
           }
     });
    //  google.maps.event.addDomListener(window, 'load', initialize);
}

// var request = {
//     // origin: new google.maps.LatLng(27.7279, 85.3284),
//     // destination: new google.maps.LatLng(28.570317, 77.321820),
//     origin: {lat: 27.7279, lng: 85.3284},
//     destination: {lat: 28.570317, lng: 77.321820},
//     travelMode: google.maps.DirectionsTravelMode.DRIVING
//  }
//  var directionsService = new google.maps.DirectionsService();
//  directionsService.route(request, function(response, status) {
//        if (status === google.maps.DirectionsStatus.OK) {
//         new google.maps.DirectionsRenderer({
//             map: map,
//             directions: response
//           });
//            // For each route, display summary information.
//        } else {
//            console.log('Directions request failed due to ' + status, response);
//        }
//  });

//darkStyle=[{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]

// This sample uses the Autocomplete widget to help the user select a
// place, then it retrieves the address components associated with that
// place, and then it populates the form fields with those details.
// This sample requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script
// src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

var placeSearch, autocomplete;

function initAutocomplete() {
  // Create the autocomplete object, restricting the search predictions to
  // geographical location types.
  autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'), {types: ['geocode']});

  // Avoid paying for data that you don't need by restricting the set of
  // place fields that are returned to just the address components.
  autocomplete.setFields(['address_component','geometry']);

  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  // autocomplete.addListener('place_changed', fillInAddress);
  autocomplete.addListener('place_changed', showPath);
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle(
          {center: geolocation, radius: position.coords.accuracy});
      autocomplete.setBounds(circle.getBounds());
    });
  }
}


// Function to get the current location of the bike
function getLocation(){
  if(navigator.geolocation){
     // timeout at 60000 milliseconds (60 seconds)
     var options = {timeout:60000};
     navigator.geolocation.getCurrentPosition
     (showLocation, errorHandler, options);
  } else{
     alert("Sorry, browser does not support geolocation!");
  }
}

// Function to show the current location on the map given the position
function showLocation(position) {
  // console.log(position);
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  let mapLocation = {lat: latitude, lng: longitude};
  currentPosition = mapLocation;
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  map = new google.maps.Map(document.getElementById('slide-map'), {
    center: mapLocation,
    disableDefaultUI: true,
    scaleControl: true,
    zoom: 18,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    // styles: darkStyle
    styles: [{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}]
});

// The marker, positioned at the <position>
var marker = new google.maps.Marker({position: mapLocation, map: map});
directionsRenderer.setMap(map);
directionsRenderer.setPanel(document.getElementById('directions-panel'));
}

function errorHandler(err) {
  if(err.code == 1) {
     alert("Error: Access is denied!");
  } else if( err.code == 2) {
     alert("Error: Position is unavailable!");
  }
}

function showPath() {
  // Get the place details from the autocomplete object.
let place = autocomplete.getPlace();
// console.log(place)
if (!place.geometry) {
  window.alert("Autocomplete's returned place contains no geometry");
  return;
}
var latitude = place.geometry.location.lat();
var longitude = place.geometry.location.lng();
let mapLocation = { lat: latitude, lng: longitude};

var request = {
    // origin: new google.maps.LatLng(27.7279, 85.3284),
    // destination: new google.maps.LatLng(28.570317, 77.321820),
    origin: currentPosition,
    destination: {lat: latitude, lng: longitude},
    travelMode: google.maps.DirectionsTravelMode.DRIVING,
    drivingOptions: {departureTime: new Date(Date.now()),trafficModel: 'optimistic'}
 }
 document.getElementById('slide-image-bike').style.display = 'none';
 directionsService.route(request, function(response, status) {
       if (status === google.maps.DirectionsStatus.OK) {
        directionsRenderer.setDirections(response);
          console.log(response);
          console.log(response.routes[0].legs[0].duration.text);
          console.log(response.routes[0].legs[0].distance.text);
           // For each route, display summary information.
       } else {
           console.log('Directions request failed due to ' + status, response);
       }
 });
 searchField.blur();
//  google.maps.event.addDomListener(window, 'load', initialize);
}

getLocation();