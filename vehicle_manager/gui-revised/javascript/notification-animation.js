const hibeam = document.getElementById('notification-hibeam');
const lowbeam = document.getElementById('notification-lowbeam');
const leftSideLight = document.getElementById('notification-leftsidelight');
const rightSideLight = document.getElementById('notification-rightsidelight');


function activateLeftSideLight(value){
    if(value == true){
        leftSideLight.style.display = 'block';
    }
    else{
        leftSideLight.style.display = 'none';
    }
}
function activateRightSideLight(value){
    if(value == true){
        rightSideLight.style.display = 'block';
    }
    else{
        rightSideLight.style.display = 'none';
    }
}
function activateHibeam(value){
    if(value == true){
        hibeam.style.display = 'block';
    }
    else{
        hibeam.style.display = 'none';
    }
}
function activateLowbeam(value){
    if(value == true){
        lowbeam.style.display = 'block';
    }
    else{
        lowbeam.style.display = 'none';
    }
}