var canvas = document.getElementById("carbon-canvas");
var ctx = canvas.getContext('2d');

// Global Options:
Chart.defaults.global.defaultFontColor = 'black';
Chart.defaults.global.defaultFontSize = 16;

var data = {
  // labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"],
  labels: [ ],
  datasets: [{
      label: "Last 31 rides",
      fill: false,
      lineTension: 0.1,
      backgroundColor: "rgba(225,0,0,0.4)",
      borderWidth: 7,
      borderColor: 'rgba(48, 213, 200, 0.6)', // The main line color
      borderCapStyle: 'butt',
    //   borderDash: [], // try [5, 15] for instance
    //   borderDashOffset: 0.0,
    //   borderJoinStyle: 'miter',
    //   pointBorderColor: "black",
    //   pointBackgroundColor: "white",
    //   pointBorderWidth: 1,
    //   pointHoverRadius: 8,
    //   pointHoverBackgroundColor: "yellow",
    //   pointHoverBorderColor: "brown",
    //   pointHoverBorderWidth: 2,
      pointRadius: 0,
      pointHitRadius: 10,
      // notice the gap in the data and the spanGaps: true
      data: [ ],
      spanGaps: true,
  }

  ]
};

// Notice the scaleLabel at the same level as Ticks
var options = {
    legend:{
        display: false
    },
    scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                    maxTicksLimit: 7,
                    display: false
                },
                scaleLabel: {
                     display: false,
                  },
                gridLines: {
                    drawBorder: false,
                    lineWidth: 2,
                    drawTicks: false,
                    zeroLineColor: '#6A6A6A',
                    zeroLineWidth: 10
                }
            }],
            xAxes: [{
                gridLines: {
                    // drawBorder: true,
                    display: false,
                    drawTicks: false,
                    zeroLineColor: 'lime',
                    zeroLineWidth: 10
                },
                ticks:{
                    display: false
                }
            }]        
        }  
};

// Chart declaration:
var carbonChart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: options
});

function addCarbonData(label, data) {
  // if(chart.data.labels.length >= 31){
  //     chart.data.labels.shift();
  //     chart.data.labels.push(label);
  // }
  let chart = carbonChart;
  chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
      if(dataset.data.length > 30){
          dataset.data.shift();
      }
  });
  chart.update();
}

function updateCarbonData(label, item) {
  let chart = carbonChart;
  let sameData = false;
  if(label == chart.data.labels[chart.data.labels.length - 1]){
    sameData = true;
  }

  if(sameData == false){
    chart.data.labels.push(label);
    if(chart.data.labels.length > 30){
      chart.data.labels.shift();
    }
  }

  chart.data.datasets.forEach((dataset) => {
    if(sameData == true){
      dataset.data.pop();
    }
    dataset.data.push(item);
    if(dataset.data.length > 30){
        dataset.data.shift();
    }
  });
  chart.update();
}

function removeCarbonData() {
  let chart = carbonChart;
  chart.data.labels.pop();
  chart.data.datasets.forEach((dataset) => {
      dataset.data.pop();
  });
  chart.update();
}

function updateCarbonOffset(coSum, data){
  var codata = data;

  updateTheTotalCarbonOffset(coSum);
  
  codata.forEach(item => {
    updateCarbonData(item[0], item[1]);
    console.log(item);
    document.getElementById('js-carbon-today').innerHTML = item[0]
  });
  if(data.length > 1){
    console.log(data)
    document.getElementById('js-carbon-start-date').innerHTML = data[0][0]
  }
}

function updateTheTotalCarbonOffset(data){
  if(data < 1000){
    document.getElementById('js-carbon-fuel-value').innerHTML = data + 'g';
  }
  else if(data/1000 < 1000){
    document.getElementById('js-carbon-fuel-value').innerHTML = Math.round(data/1000, 1) + 'kg';
  }
}

eel.expose(updateFuelSavings);
function updateFuelSavings(data){
  document.getElementById('js-carbon-savings-value').innerHTML = data;
}

