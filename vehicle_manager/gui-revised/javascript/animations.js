let currentMode = 'MODE_STANDBY';
let modeTextLeft = document.getElementById('mode-text-left');
let modeTextMiddle = document.getElementById('mode-text-middle');
let modeTextRight = document.getElementById('mode-text-right');
let modeChargingWave = document.getElementById('mode-wave-container');

let speedBarForward = document.getElementById('mode-line-speed-forward');
let speedBarReverse = document.getElementById('mode-line-speed-reverse');
let statusSpeed = document.getElementById('speed-status-value');

function setMode(mode){
    currentMode = mode;
    if(mode == 'MODE_STANDBY'){
        modeTextLeft.style.opacity = 0;
        modeTextRight.style.opacity = 0;
        modeTextMiddle.innerHTML = 'STANDBY';
        modeTextMiddle.style.color = '#000000';
        modeTextMiddle.style.fontWeight = 'bold';
        modeChargingWave.style.display = 'none';

        // Speed Bar
        speedBarForward.style.display = 'none';
        speedBarReverse.style.display = 'none';
    }
    else if(mode == 'MODE_THIKKA'){
        modeTextLeft.style.opacity = 1;
        modeTextRight.style.opacity = 1;
        modeTextMiddle.innerHTML = 'THIKKA';
        modeTextMiddle.style.color = '#000000';
        modeTextMiddle.style.fontWeight = 'bold';
        modeChargingWave.style.display = 'none';
        // Speed Bar
        speedBarForward.style.display = 'block';
        speedBarReverse.style.display = 'none';
    }
    else if(mode == 'MODE_SUSTE'){
        modeTextLeft.style.opacity = 1;
        modeTextRight.style.opacity = 1;
        modeTextMiddle.innerHTML = 'THIKKA';

        modeTextLeft.style.fontWeight = 'bold';
        modeTextLeft.style.color = '#000000';

        modeTextMiddle.style.fontWeight = 'normal';
        modeTextMiddle.style.color = '#AEAEAE';

        modeTextRight.style.fontWeight = 'normal';
        modeTextRight.style.color = '#AEAEAE';
        modeChargingWave.style.display = 'none';
    }
    else if(mode == 'MODE_BABBAL'){
        modeTextLeft.style.opacity = 1;
        modeTextRight.style.opacity = 1;
        modeTextMiddle.innerHTML = 'THIKKA';

        modeTextLeft.style.fontWeight = 'normal';
        modeTextLeft.style.color = '#AEAEAE';

        modeTextMiddle.style.fontWeight = 'normal';
        modeTextMiddle.style.color = '#AEAEAE';

        modeTextRight.style.fontWeight = 'bold';
        modeTextRight.style.color = '#000000';
        modeChargingWave.style.display = 'none';
    }
    else if(mode == 'MODE_REVERSE'){
        modeTextLeft.style.opacity = 0;
        modeTextRight.style.opacity = 0;
        modeTextMiddle.innerHTML = 'REVERSE';
        modeTextMiddle.style.color = '#000000';
        modeTextMiddle.style.fontWeight = 'bold';
        modeChargingWave.style.display = 'none';
        // Speed Bar
        speedBarForward.style.display = 'none';
        speedBarReverse.style.display = 'block';
    }
    else if(mode == 'MODE_CHARGING'){
        modeTextLeft.style.opacity = 0;
        modeTextRight.style.opacity = 0;
        modeTextMiddle.innerHTML = 'CHARGING';
        modeTextMiddle.style.color = '#40e0d0';
        modeTextMiddle.style.fontWeight = 'bold';
        modeChargingWave.style.display = 'block';
        // Speed Bar
        speedBarForward.style.display = 'none';
        speedBarReverse.style.display = 'none';
    }
}

const maxSpeed = 120;
const maxSpeedBarWidth = 503;
let currentSpeedBarWidth = 0;

const defaultSpeedBarOffset = 600;
let reverseSpeedBarOffset = 600;
const reverseSpeedFactor = 5;
function setSpeed(speed){
    statusSpeed.innerHTML = speed;

    if(currentMode != 'MODE_REVERSE'){
        currentSpeedBarWidth = speed/maxSpeed * maxSpeedBarWidth;
        speedBarForward.style.width = currentSpeedBarWidth + 'px';
    }
    if(currentMode == 'MODE_REVERSE'){
        currentSpeedBarWidth = speed/maxSpeed * maxSpeedBarWidth * reverseSpeedFactor;
        speedBarReverse.style.width = currentSpeedBarWidth + 'px';

        reverseSpeedBarOffset = defaultSpeedBarOffset - currentSpeedBarWidth;
        speedBarReverse.style.left = reverseSpeedBarOffset + 'px';
    }
}