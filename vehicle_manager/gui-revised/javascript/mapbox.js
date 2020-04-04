mapboxgl.accessToken = 'pk.eyJ1IjoieWF0cmkiLCJhIjoiY2swZzY1MDNqMDQ2ZzNubXo2emc4NHZwYiJ9.FtepvvGORqK03qJxFNvlEQ';
var destinationMarker = new mapboxgl.Marker({
  draggable: true
});
let destination;
let route;
var map = new mapboxgl.Map({
    container: 'slide-map', // container id
    // style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
    // style: 'mapbox://styles/yatri/ck7ligoue0ikz1ipejlvssxf0',
    style: 'mapbox://styles/yatri/ck7n2g8mw0mf41ipgdkwglthq',
    center: [85.324, 27.717], // starting position [lng, lat]
    zoom: 16 // starting zoom
    });


// Add a Geocoder to the map
var geocoder = new MapboxGeocoder({ // Initialize the geocoder
    accessToken: mapboxgl.accessToken, // Set the access token
    // types: 'poi',
    countries: 'NP',
    collapsed: true,
    clearOnBlur: true,
    // render: function(item) {
    //     // extract the item's maki icon or use a default
    //     var maki = item.properties.maki || 'marker';
    //     return (
    //     "<div class='geocoder-dropdown-item'><img class='geocoder-dropdown-icon' src='https://unpkg.com/@mapbox/maki@6.1.0/icons/" +
    //     maki +
    //     "-15.svg'><span class='geocoder-dropdown-text'>" +
    //     item.text +
    //     '</span></div>'
    //     );
    //     },
    mapboxgl: mapboxgl, // Set the mapbox-gl instance
    marker: false, // Do not use the default marker style
    // marker: {
    //   color: 'red'
    //   },
    // proximity: {
    //     longitude: 85.324,
    //     latitude: 27.717
    //   }
  });
  
  // Add the geocoder to the map
  map.addControl(geocoder);
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
  
    // map.addLayer({
    //   id: 'point',
    //   source: 'single-point',
    //   type: 'circle',
    //   paint: {
    //     'circle-radius': 10,
    //     'circle-color': '#448ee4'
    //   }
    // });

  
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
    // var coords = Object.keys(coordsObj).map(function(key) {
    //   return coordsObj[key];
    // });
    var end = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'Point',
          coordinates: coordsObj
        }
      }
      ]
    };

    destinationMarker.setLngLat(coordsObj)
    .addTo(map);
    // if (map.getLayer('end')) {
    //   map.getSource('end').setData(end);
    // } else {
    //   map.addLayer({
    //     id: 'end',
    //     type: 'circle',
    //     source: {
    //       type: 'geojson',
    //       data: {
    //         type: 'FeatureCollection',
    //         features: [{
    //           type: 'Feature',
    //           properties: {},
    //           geometry: {
    //             type: 'Point',
    //             coordinates: coordsObj
    //           }
    //         }]
    //       }
    //     },
    //     paint: {
    //       'circle-radius': 10,
    //       'circle-color': '#40e0d0'
    //     }
    //   });
    // }
    getRoute(coordsObj);
    });
  });
  

// initialize the map canvas to interact with later
var canvas = map.getCanvasContainer();

// an arbitrary start will always be the same
// only the end or destination will change
var start = [85.324, 27.717];

// Current Location Marker
var marker = new mapboxgl.Marker() // initialize a new marker
  .setLngLat(start) // Marker [lng, lat] coordinates
  .addTo(map); // Add the marker to the map

// create a function to make a directions request
function getRoute(end) {
    // make a directions request using cycling profile
    // an arbitrary start will always be the same
    // only the end or destination will change
    var start = [85.324, 27.717];
    var url = 'https://api.mapbox.com/directions/v5/mapbox/driving/' + start[0] + ',' + start[1] + ';' + end[0] + ',' + end[1] + '?steps=true&geometries=geojson&access_token=' + mapboxgl.accessToken;
  
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
  
  map.on('load', function() {
    // make an initial directions request that
    // starts and ends at the same location
    getRoute(start);
  });

function addPlaceToPanel(place){
    let content = place;
     document.getElementById('summary-label').innerHTML = content;
     document.getElementById('summary-box').style.display = 'block';
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

  function onDragEnd() {
    var lngLat = marker.getLngLat();
    // coordinates.style.display = 'block';
    // coordinates.innerHTML =
    // 'Longitude: ' + lngLat.lng + '<br />Latitude: ' + lngLat.lat;
    let markerCoord = [lngLat.lng, lngLat.lat];
    console.log(markerCoord);
    getRoute(markerCoord);
    }

    function onRotateEnd() {
      let bearing = -map.getBearing();
      console.log(bearing);
      document.getElementById("navigation-north").style.transform = "rotate("+bearing+"deg)";
    }
    destinationMarker.on('dragend',onDragEnd);
    map.on('rotateend', onRotateEnd);
    document.getElementById('navigation-north').addEventListener('click', function(){
      map.resetNorth();
    })