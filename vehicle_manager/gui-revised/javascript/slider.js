$slide=0;
$clickDisabled=0;
$clickTimeout = 750;

// Carousel in the User Slide
$(document).ready(function(){
    // Cycles to the next item
    $("#right-slider").click(function(){
        if($clickDisabled == 0){
            $clickDisabled = 1;
            $("#slider-one").carousel('next');
            $slide = $slide + 1;
            if($slide == 1){
                $('#left-slider').css("display","block");
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
    // Cycles to the previous item
      $("#left-slider").click(function(){
        if($clickDisabled == 0){
            $clickDisabled=1;
            $("#slider-one").carousel('prev');
            $slide = $slide - 1;
            if($slide == 0){
                $('#left-slider').css("display","none");
                $('#right-slider-content').attr('src', 'icons/slider-map-right.svg')
            }
            else if($slide == 1){
                $('#right-slider').css("display","block");
                $('#left-slider-content').attr('src', 'icons/slider-home-left.svg')
                $('#right-slider-content').attr('src', 'icons/slider-stats-right.svg')
            }
            setTimeout(function(){
                $clickDisabled=0;
            }, $clickTimeout)
        }
      });
  });

//   $("#slider-one").carousel('next');
//             $slide = $slide + 1;
//             if($slide == 1){
//                 $('#left-slider').css("display","block");
//             }
//             else if($slide == 2){
//                 $('#right-slider').css("display","none");
//                 $('#left-slider-content').attr('src', 'icons/slider-map-left.svg')
//             }