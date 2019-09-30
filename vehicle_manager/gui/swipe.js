var myElement = document.getElementById('yatri-logo-2');

// create a simple instance
// by default, it only adds horizontal recognizers
var mc = new Hammer(myElement);

// hammertime.get('swipeleft')
// listen to events...
mc.on("swipeleft swiperight tap", function(ev) {
    console.log(ev.type +" gesture detected.");
});

mc.on("swipeleft", function(){
    slideRight();
});
mc.on("swiperight", function(){
    slideLeft();
});