$(document).ready(function(){
    // Cycles to the next item
    $("#reboot-computer").click(function(){
        console.log('Rebooting Computer');
            eel.rebootBoard();
      });

      $("#ten-min").click(function(){
        eel.startFastCharge(1);   
      });
    $("#thirty-min").click(function(){
      eel.startFastCharge(3);   
    });
    $("#sixty-min").click(function(){
      eel.startFastCharge(6);   
    });
    $("#seventy-min").click(function(){
      eel.startFastCharge(7);   
    });
    $("#stop-charging").click(function(){
      eel.startFastCharge(0);   
    });
      $("#refresh").click(function(){
        console.log('Refreshing Engineering Menu')
        eel.getConnectivityStatus();   
    });
});

const enggConnectivityStatus = document.getElementById('engg-connectivity-status');
const enggIPAddress = document.getElementById('engg-ip-address');

eel.expose(updateConnectivityStatus)
function updateConnectivityStatus(iface, ip){
  enggConnectivityStatus.innerHTML = iface;
  enggIPAddress.innerHTML = ip;
}

eel.expose(updatePackVoltage);
function updatePackVoltage(voltage){
  document.getElementById('engg-battery-status').innerHTML = voltage;
}