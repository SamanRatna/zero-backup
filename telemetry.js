// Initialize variables
count = 0;
// power = 0;
// speed = 0;
// range = 0;

var getData = function(){
    // Setup ajax request and get data as 'response'
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(xhttp.responseText);
            bat_current = response.bat_current;
            bat_voltage = response.bat_voltage;
            veh_speed = response.veh_speed;
            max_torque = response.max_torque;
            torque_act = response.torque_act;
            motor_temp = response.motor_temp;
            motor_vel = response.motor_vel;
            drive_prof = response.drive_prof;
            trip_dist = response.trip_dist;
            htsink_temp = response.htsink_temp;
            dig_input = response.dig_input;
            console.log(bat_current, bat_voltage);

            // Display telemetry data
            document.getElementById('bat_current').innerHTML = bat_current;
            document.getElementById('bat_voltage').innerHTML = bat_voltage;
            document.getElementById('veh_speed').innerHTML = veh_speed;
            document.getElementById('max_torque').innerHTML = max_torque;
            document.getElementById('torque_act').innerHTML = torque_act;
            document.getElementById('motor_temp').innerHTML = motor_temp;
            document.getElementById('motor_vel').innerHTML = motor_vel;
            document.getElementById('drive_prof').innerHTML = drive_prof;
            document.getElementById('trip_dist').innerHTML = trip_dist;
            document.getElementById('htsink_temp').innerHTML = htsink_temp;
            document.getElementById('dig_input').innerHTML = dig_input;
        }
    };

    // Load data
    xhttp.open("GET", "data.json", true)
    xhttp.send();
}

// Run getData at a certain time interval
setInterval(getData, 50)

