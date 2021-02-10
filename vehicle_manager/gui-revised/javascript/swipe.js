var touchstartX = 0;
var touchstartY = 0;
var touchendX = 0;
var touchendY = 0;
const threshold = 300;
var swipeZone = document.getElementById('js-logo-frame');

swipeZone.addEventListener('touchstart', function(event) {
    touchstartX = event.changedTouches[0].clientX;
}, false);

swipeZone.addEventListener('touchmove', function(event){
    let currentTouch = event.changedTouches[0].clientX;
    let swipeDiff = currentTouch - touchstartX;
    if(swipeDiff < 0){
        if(Math.abs(swipeDiff)>threshold){
            document.getElementById('js-navigation-toggle').classList.add('navigation-bubble-animation');
        } else{
            document.getElementById('js-navigation-toggle').classList.remove('navigation-bubble-animation');
        }
    }
    else if(swipeDiff > 0){
        if(Math.abs(swipeDiff)>threshold){
            document.getElementById('js-home-toggle').classList.add('home-bubble-animation');
        } else{
            document.getElementById('js-home-toggle').classList.remove('home-bubble-animation');
        }
    }
}, false);

swipeZone.addEventListener('touchend', function(event) {
    touchendX = event.changedTouches[0].clientX;
    handleGesture();
}, false); 

function handleGesture() {
    // console.log(touchstartX, touchendX);
    document.getElementById('js-navigation-toggle').classList.remove('navigation-bubble-animation');
    document.getElementById('js-home-toggle').classList.remove('home-bubble-animation');

    if(Math.abs(touchendX - touchstartX) > threshold){
        console.log('Handling Swipe')
        if(touchendX < touchstartX){ // go to navigation mode
            if(uiMode != 'map-mode'){
                switchUIMode();
            }
        } else{ // go to home screen
            if(uiMode != 'no-map-mode'){
                switchUIMode();
            }
        }
    } else {
        console.log('Swipe too short')
    }
}
