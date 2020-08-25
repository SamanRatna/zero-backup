document.getElementById('js-speed-unit-toggle').addEventListener('click', function(){
    document.getElementById('js-speed-label-km').classList.toggle('active');
    document.getElementById('js-speed-label-mile').classList.toggle('active');
    document.getElementById('js-speed-unit-button').classList.toggle('toggled');
});

document.getElementById('js-temperature-unit-toggle').addEventListener('click', function(){
    document.getElementById('js-temperature-label-c').classList.toggle('active');
    document.getElementById('js-temperature-label-f').classList.toggle('active');
    document.getElementById('js-temperature-unit-button').classList.toggle('toggled');
});