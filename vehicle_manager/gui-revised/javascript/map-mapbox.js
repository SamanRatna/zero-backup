L.mapbox.accessToken = 'pk.eyJ1IjoieWF0cmkiLCJhIjoiY2swZzY1MDNqMDQ2ZzNubXo2emc4NHZwYiJ9.FtepvvGORqK03qJxFNvlEQ';
var mapBoxUrl = 'https://api.mapbox.com/styles/v1/shavitamit/cintinlry003wzvnl4e8mv498/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic2hhdml0YW1pdCIsImEiOiJjaW5zNmJxM2cxMHFudHFram4wMWR5cWc2In0.8iSMtmKveklyOiEI1WjA5A';

var mapboxTiles = L.tileLayer(mapBoxUrl, {
  attribution: '© <a href="https://www.mapbox.com/map-feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  tileSize: 512,
  zoomOffset: -1
});
var map = L.mapbox.map('slide-map')
    .setView([27.727, 85.328], 13)
    .addLayer(mapboxTiles)
    .addControl(L.mapbox.geocoderControl('mapbox.places', {
      autocomplete: true
  }));

// create the initial directions object, from which the layer
// and inputs will pull data.
var directions = L.mapbox.directions();

var directionsLayer = L.mapbox.directions.layer(directions)
    .addTo(map);

var directionsInputControl = L.mapbox.directions.inputControl('inputs', directions)
    .addTo(map);

var directionsErrorsControl = L.mapbox.directions.errorsControl('errors', directions)
    .addTo(map);

var directionsRoutesControl = L.mapbox.directions.routesControl('routes', directions)
    .addTo(map);

var directionsInstructionsControl = L.mapbox.directions.instructionsControl('instructions', directions)
    .addTo(map);