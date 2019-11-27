
var speedData = {
    datasets: [{
        backgroundColor: [
        "#3B3EAC"],
        // hoverBackgroundColor: [
        // "#3366CC",
        // "#DC3912",
        // "#FF9900",
        // "#109618",
        // "#990099",
        // "#3B3EAC"
        // ],
        data: [
        84.69,
        ]
    },
    {
        backgroundColor: [
        "#990099"],
        // hoverBackgroundColor: [
        // "#3366CC",
        // "#DC3912",
        // "#FF9900",
        // "#109618",
        // "#990099",
        // "#3B3EAC"
        // ],
        data: [
        84.69,
        ]
    },
    {
        backgroundColor: [
        "#109618"],
        // hoverBackgroundColor: [
        // "#3366CC",
        // "#DC3912",
        // "#FF9900",
        // "#109618",
        // "#990099",
        // "#3B3EAC"
        // ],
        data: [
        95.96
        ]
    }],
    labels: [
    "resource-group-1",
    "resource-group-2",
    "Data Services - Basic Database Days",
    "Data Services - Basic Database Days",
    "Azure App Service - Basic Small App Service Hours",
    "resource-group-2 - Other"
    ]
}
var speedOptions = {
    rotation: 1.5 * Math.PI,
    circumference: 1 * Math.PI
}
var resourceChartElement = document.getElementById("speed-canvas-1");
var resourceChart = new Chart(resourceChartElement, {
    type: "doughnut",
    data: speedData,
    options: speedOptions
});

