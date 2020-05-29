let brightnessPanel = document.getElementById('yatri-logo-id');
let brightnessControl = new Hammer(brightnessPanel);
brightnessControl.get('pan').set({ direction: Hammer.DIRECTION_HORIZONTAL });
let currentBrightness = 50;

brightnessControl.on('pan', function(ev) {
    // console.log(ev.deltaX);
    calculateBrightness(ev.deltaX);
});

function calculateBrightness(delta){
    currentBrightness = currentBrightness + Math.round(delta/200);
    currentBrightness = currentBrightness>100 ? 100 : currentBrightness<1 ? 1 : currentBrightness;
    // console.log(currentBrightness);
    eel.changeBrightness(currentBrightness);
}

