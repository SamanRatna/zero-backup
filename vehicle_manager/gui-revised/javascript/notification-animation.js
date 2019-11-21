const hibeam = document.getElementById('notification-hibeam');
const lowbeam = document.getElementById('notification-lowbeam');
const leftSideLight = document.getElementById('notification-leftsidelight');
const rightSideLight = document.getElementById('notification-rightsidelight');

// eel.expose(activateLeftSideLight)
// function activateLeftSideLight(value){
//     if(value == true){
//         leftSideLight.style.display = 'block';
//     }
//     else{
//         leftSideLight.style.display = 'none';
//     }
// }

// eel.expose(activateRightSideLight)
// function activateRightSideLight(value){
//     if(value == true){
//         rightSideLight.style.display = 'block';
//     }
//     else{
//         rightSideLight.style.display = 'none';
//     }
// }

// eel.expose(activateHibeam)
// function activateHibeam(value){
//     if(value == true){
//         hibeam.style.display = 'block';
//     }
//     else{
//         hibeam.style.display = 'none';
//     }
// }

// eel.expose(activateLowbeam)
// function activateLowbeam(value){
//     if(value == true){
//         lowbeam.style.display = 'block';
//     }
//     else{
//         lowbeam.style.display = 'none';
//     }
// }

eel.expose(updateBeam);
function updateBeam(status){
    if(status == 'off'){
        lowbeam.style.display = 'none';
        hibeam.style.display = 'none';
    }
    else if(status == 'high'){
        lowbeam.style.display = 'none';
        hibeam.style.display = 'block';
    }
    else if(status == 'low'){
        lowbeam.style.display = 'block';
        hibeam.style.display = 'none';
    }
}

eel.expose(updateSideLight);
function updateSideLight(status){
    if(status == 'off'){
        leftSideLight.style.display = 'none';
        rightSideLight.style.display = 'none';
    }
    else if(status == 'right'){
        leftSideLight.style.display = 'none';
        rightSideLight.style.display = 'block';
    }
    else if(status == 'left'){
        leftSideLight.style.display = 'block';
        rightSideLight.style.display = 'none';
    }
    else if(status == 'both'){
        leftSideLight.style.display = 'block';
        rightSideLight.style.display = 'block';
    }
}