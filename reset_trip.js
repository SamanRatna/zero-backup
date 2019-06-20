
var resetTrip = function(){
    // Setup ajax request and get data as 'response'
    /*
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(xhttp.responseText);
            odometer = response.trip_dist;
            console.log(odometer)

            let xhr = new XMLHttpRequest();

            let trip_json = {
              "trip_dist": odometer
            };

            xhr.open("POST", 'trip.json', true)
            xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            xhr.send(trip_json);
        }
    }

    // Load data
    xhttp.open("GET", "data.json", true)
    xhttp.send();

    */
    document.getElementById('trip_dist').innerHTML = "This will be reset";

}
