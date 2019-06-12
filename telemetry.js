// Initialize variables
count = 0;
power = 0;
speed = 0;
range = 0;

var getData = function(){
    // Setup ajax request and get data as 'response'
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(xhttp.responseText);
            power = response.power;
            speed = response.speed;
            range = response.range;
            console.log(power, speed, range);

            // Display telemetry data
            document.getElementById('power').innerHTML = power;
            document.getElementById('speed').innerHTML = speed;
            document.getElementById('range').innerHTML = range;
        }
    };

    // Load data
    xhttp.open("GET", "data.json", true)
    xhttp.send();
}

// Run getData at a certain time interval
setInterval(getData, 20)
