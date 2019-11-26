var data = {
    labels: ["BATTERY", "CONTROLLER", "ECU", "AMBIENT", "MOTOR"],
    datasets: [{
        borderColor: 'rgba(48, 213, 200, 0.6)',
        borderWidth: 8,
        fill: true,
        backgroundColor: 'rgba(48, 213, 200, 0.2)',
        data: [30, 40, 50, 30, 20]
    }]
};

Chart.defaults.global.defaultFontColor = '#fff';

var options = {
    maintainAspectRatio: false,
    legend: {
        display: false
    },
    // tooltips: {
    //     enabled: true
    // },
    scale: {
        reverse: false,
        gridLines: {
            display: true,
            circular: true,
            lineWidth: 5
        },
        angleLines: {
            display: true,
            lineWidth: 5
        },
        ticks: {
            display: true,
            fontSize: 50,
            fontColor: '#666',
            fontFamily: 'Barlow',
            fontStyle: 'bold',
            stepSize: 10,
            beginAtZero: false,
            min: 1,
            max: 70,
            maxTicksLimit: 5,
            lineHeight: 50
        },
        pointLabels: {
            display: true,
            fontSize: 50,
            fontFamily: 'Barlow',
            fontStyle: 'bold',
            fontColor: '#666'
            // fontStyle: 'mons-regular'
        },
    },
    elements: {
        point: {
              radius: 0
        }
    }
};

var chart = new Chart('temperature-canvas', {
    type: 'radar',
    data: data,
    options: options
});

// function changeRed() { 
//   chart.data.datasets[1].data = [1, 5, 2, 3, 4];
//   chart.update();
// }
