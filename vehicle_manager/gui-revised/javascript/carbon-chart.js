var canvas = document.getElementById("carbon-canvas");
var ctx = canvas.getContext('2d');

// Global Options:
Chart.defaults.global.defaultFontColor = 'black';
Chart.defaults.global.defaultFontSize = 16;

var data = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  datasets: [{
      label: "Stock A",
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
    //   pointHitRadius: 10,
      // notice the gap in the data and the spanGaps: true
      data: [0, 59, 80, 81, 56, 55, 40, ,60,55,30,78],
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
                    lineWidth: 4,
                    drawTicks: false,
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
var myBarChart = new Chart(ctx, {
  type: 'line',
  data: data,
  options: options
});