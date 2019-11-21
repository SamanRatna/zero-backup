// plusSlides(1);

setMode('MODE_THIKKA');

//Speed Generator Function
var dMode = 0;
var dSpeed = 0;
function speedGenerator(){
    if(dMode == 0){
        dSpeed = (dSpeed + 2)
        if(currentMode != 'MODE_REVERSE'){
        if(dSpeed > 119){
            dMode=1;
        }
        }
        else{
            if(dSpeed > 15){
                dMode=1;
            }
        }
    }
    else if(dMode == 1){
        dSpeed = dSpeed - 3;
        if(dSpeed < 1){
            dMode = 0;
            if( Math.round(Math.random()) == 0){
                setMode('MODE_THIKKA');
            }
            else {
                setMode('MODE_REVERSE');
            }
        }
    }
}

setInterval(function(){   
    speedGenerator();
    setSpeed(dSpeed);
}, 50);

//signal-demo
