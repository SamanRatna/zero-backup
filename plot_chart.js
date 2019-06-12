// Plot chart
var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'X',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.0)',
                'rgba(54, 162, 235, 0.0)',
                'rgba(255, 206, 86, 0.0)',
                'rgba(75, 192, 192, 0.0)',
                'rgba(153, 102, 255, 0.0)',
                'rgba(255, 159, 64, 0.0)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
               animation: {
                   duration: 0
               },
               responsive: false,
               scales: {
                   yAxes: [{
                       display: false,
                       ticks: {
                           beginAtZero: true,
                           max: 25,
                           display: false
                       },
                       gridLines: {
                           display: false
                       }
                   }],
                   xAxes: [{
                       display: false,
                       ticks: {
                           display: false
                       },
                       gridLines: {
                           display: false
                       }
                   }]
               },
               legend: {
                   display: false
               },
               tooltips: {
                   enabled: false
               }
           }
});

// Initialize variables
count = 0;
power = 0;
speed = 0;
range = 0;

// Define function to get data and update chart
var getData = function(){
    // Setup ajax request and get data as 'response'
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(xhttp.responseText);
            power = response.power;
            // console.log(power);

        }
    };

    // Load data
    xhttp.open("GET", "data.json", true)
    xhttp.send();

    // Update chart
    myChart.data.labels.push(count++)
    myChart.data.datasets[0].data.push(power)

    if (myChart.data.labels.length>=70){
        myChart.data.labels.splice(0, 1)
        myChart.data.datasets[0].data.splice(0, 1)
    }
    myChart.update();
}

// Run getData at a certain time interval
setInterval(getData, 20)
