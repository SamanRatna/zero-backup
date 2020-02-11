$slide=0;
$clickDisabled=0;
$clickTimeout = 750;

// // Carousel in the User Slide
// $(document).ready(function(){
//     // Cycles to the next item
//     $("#right-slider").click(function(){
//         if($clickDisabled == 0){
//             $clickDisabled = 1;
//             $("#slider-one").carousel('next');
//             $slide = $slide + 1;
//             if($slide == 1){
//                 $('#left-slider').css("display","block");
//                 $('#right-slider-content').attr('src', 'icons/slider-stats-right.svg')
//             }
//             else if($slide == 2){
//                 $('#right-slider').css("display","none");
//                 $('#left-slider-content').attr('src', 'icons/slider-map-left.svg')
//             }
//             setTimeout(function(){
//                 $clickDisabled=0;
//             }, $clickTimeout)
//         }
//       });
//     // Cycles to the previous item
//       $("#left-slider").click(function(){
//         if($clickDisabled == 0){
//             $clickDisabled=1;
//             $("#slider-one").carousel('prev');
//             $slide = $slide - 1;
//             if($slide == 0){
//                 $('#left-slider').css("display","none");
//                 $('#right-slider-content').attr('src', 'icons/slider-map-right.svg')
//             }
//             else if($slide == 1){
//                 $('#right-slider-content').attr('src', 'icons/slider-stats-right.svg')
//                 $('#right-slider').css("display","block");
//                 $('#left-slider-content').attr('src', 'icons/slider-home-left.svg')            }
//             setTimeout(function(){
//                 $clickDisabled=0;
//             }, $clickTimeout)
//         }
//       });
//   });

//   $("#slider-one").carousel('next');
//             $slide = $slide + 1;
//             if($slide == 1){
//                 $('#left-slider').css("display","block");
//             }
//             else if($slide == 2){
//                 $('#right-slider').css("display","none");
//                 $('#left-slider-content').attr('src', 'icons/slider-map-left.svg')
//             }

//current position.
var pos = 0;
//number of slides
var totalSlides = $('#slider-wrap ul li').length;
//get the slide width
var sliderWidth = $('#slider-wrap').width();


$(document).ready(function () {
	/*****************
	 BUILD THE SLIDER
	*****************/
    //set width to be 'x' times the number of slides
    $('#slider-wrap ul#slider').width(sliderWidth * totalSlides);

    //next slide 	
    $('#right-slider').click(function () {
        if($clickDisabled == 0){
            $clickDisabled = 1;
            slideRight();
            $slide = $slide + 1;
            if($slide == 1){
                $('#left-slider').css("display","block");
                $('#right-slider-content').attr('src', 'icons/slider-stats-right.svg')
            }
            else if($slide == 2){
                $('#right-slider').css("display","none");
                $('#left-slider-content').attr('src', 'icons/slider-map-left.svg')
            }
            setTimeout(function(){
                $clickDisabled=0;
            }, $clickTimeout)
        }
    });

    //previous slide
    $('#left-slider').click(function () {
        if($clickDisabled == 0){
            $clickDisabled=1;
            slideLeft();
            $slide = $slide - 1;
            if($slide == 0){
                $('#left-slider').css("display","none");
                $('#right-slider-content').attr('src', 'icons/slider-map-right.svg')
            }
            else if($slide == 1){
                $('#right-slider-content').attr('src', 'icons/slider-stats-right.svg')
                $('#right-slider').css("display","block");
                $('#left-slider-content').attr('src', 'icons/slider-home-left.svg')            }
            setTimeout(function(){
                $clickDisabled=0;
            }, $clickTimeout)
        }
    });
});//DOCUMENT READY



/***********
 SLIDE LEFT
************/
function slideLeft() {
    pos--;
    if (pos == -1) { pos = totalSlides - 1; }
    $('#slider-wrap ul#slider').css('left', -(sliderWidth * pos));
}


/************
 SLIDE RIGHT
*************/
function slideRight() {
    pos++;
    if (pos == totalSlides) { pos = 0; }
    $('#slider-wrap ul#slider').css('left', -(sliderWidth * pos));
}

function skipToInfograph() {
    document.getElementById('right-slider').click();
}
setTimeout(function(){
    skipToInfograph();
}, 1000)
// setTimeout(function(){
//     skipToInfograph();
// }, 2000)
let navigateButton = document.getElementById("navigation-button");
let searchField = document.getElementById('autocomplete');

navigateButton.addEventListener('click', function(){
    navigateButton.style.display = 'none';
    searchField.style.display = 'flex';
    searchField.focus();
   });

function closeSearchBox(){
    searchField.style.display = 'none';
    navigateButton.style.display = 'block';
}
// searchField.addEventListener('focusout', function(){
//     searchField.style.display = 'none';
//     navigateButton.style.display = 'block';
//     clearOldSuggestions();
// });