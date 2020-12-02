
eel.expose(requestSWUpdateConfirmation);
eel.expose(updateSpeedPower);
eel.expose(updateSOC)
eel.expose(updateBikeMode);
eel.expose(updateMaxSpeed);
eel.expose(updateDistances);
eel.expose(updateAverageSpeeds);
eel.expose(updateBluetoothStatus);
eel.expose(updateAdvertisementStatus);
eel.expose(updateBluetoothDevices);
eel.expose(updateStandState);
eel.expose(updateCarbonOffset);
eel.expose(requestBluetoothPairingConfirmation);
eel.expose(updateTime);
eel.expose(updateTurnSignal);
eel.expose(updateHeadlightSignal);
eel.expose(updateStandState);
eel.expose(updateCarbonOffset);
eel.expose(updateNetworkInfo);
eel.expose(updateOrientation);
eel.expose(updateBluetoothName);

// eel.initCarbonOffset();

function updateRouteToBackend(route){
  // eel.updateRoute(route);
}
function initiateTripReset(){
  eel.resetTripData()
}

function initializeGUI(){
  eel.getGUIData()
}

function respondBluetoothPairing(response){
  eel.bluetoothPairingConfirmation(response);
}

initializeGUI();