var tripChart = document.getElementById("trip-chart");
var myChart = new Chart(tripChart, {
  type: 'pie',
  data: {
    labels: ['Current', 'Last'],
    datasets: [{
      data: [20, 100],
      backgroundColor: [
        'rgba(64, 224, 208)',
        'rgba(175, 175, 175)',
      ],
    }]
  },
  options: {
   	cutoutPercentage: 55,
    responsive: false,
  }
});
