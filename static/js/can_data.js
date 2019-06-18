function get_can() {
  // Setup AJAX request code
  var req = new XMLHttpRequest();
  req.onreadystatechange = function()
  {
    if(this.readyState == 4 && this.status == 200) {
      // Sort data 
      console.log(this.responseText)
      if(this.responseText != null){
            response = JSON.parse(this.responseText);
            console.log(response);
            bat_current = response.bat_current;
            bat_voltage = response.bat_voltage;
            veh_speed = response.veh_speed;
            max_torque = response.max_torque;
            torque_act = response.torque_act;
            motor_temp = response.motor_temp;
            motor_vel = response.motor_vel;
            drive_prof = response.drive_prof;
            odometer = response.odometer;
            htsink_temp = response.htsink_temp;
            dig_input = response.dig_input;
            s_o_charge = response.s_o_charge;
            est_range = response.est_range;
            recuperation = response.recuperation;

            // Display telemetry data
            document.getElementById('bat_current').innerHTML = bat_current;
            document.getElementById('bat_voltage').innerHTML = bat_voltage;
            document.getElementById('veh_speed').innerHTML = veh_speed;
            document.getElementById('max_torque').innerHTML = max_torque;
            document.getElementById('torque_act').innerHTML = torque_act;
            document.getElementById('motor_temp').innerHTML = motor_temp;
            document.getElementById('motor_vel').innerHTML = motor_vel;
            document.getElementById('drive_prof').innerHTML = drive_prof;
            document.getElementById('odometer').innerHTML = odometer;
            document.getElementById('htsink_temp').innerHTML = htsink_temp;
            document.getElementById('dig_input').innerHTML = dig_input;
            document.getElementById('s_o_charge').innerHTML = s_o_charge;
            document.getElementById('est_range').innerHTML = est_range;
            document.getElementById('recuperation').innerHTML = recuperation;
      }
    }
  }

  // Load data
  req.open('POST', '/', true);
  // req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  req.send();
}

// Run get_can at a certain interval
setInterval(get_can, 100)
