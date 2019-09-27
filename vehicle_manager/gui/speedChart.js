var speedCanvas = document.getElementById('speed-chart');

// Chart.defaults.global.defaultFontFamily = "Lato";
// Chart.defaults.global.defaultFontSize = 18;

var speedData = {
  labels: ["0s", "10s", "20s", "30s", "40s", "50s", "60s", "0s", "10s", "20s", "30s", "40s", "50s", "60s"],
  datasets: [{
    label: "Speed (kmph)",
    data: [],
    backgroundColor: "rgba(64,224,208,0.6)",
    // fill:false
  }]
};

var chartOptions = {
  legend: {
    display: true,
    position: 'bottom',
    labels: {
      boxWidth: 40,
      fontColor: 'black'
    }
  },
  layout: {
    padding: {
        top: 20,
    }
  },
  scales: {
    yAxes: [{
        ticks: {
            // beginAtZero: true,
        },
        // gridLines: {
        //     display:false,
        // }
    }],
    xAxes: [{
        ticks: {
            display: false,
            },
        gridLines: {
            display:false,
        }
    }]
  },
  elements: {
    point:{
        radius: 0
    }
  }
};

var speedChart = new Chart(speedCanvas, {
  type: 'line',
  data: speedData,
  options: chartOptions
});

function addData(chart, label, data) {
    if(chart.data.labels.length = 100){
        chart.data.labels.shift();
        chart.data.labels.push(label);
    }
    
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
        if(dataset.data.length >= 100){
            dataset.data.shift();
        }
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}