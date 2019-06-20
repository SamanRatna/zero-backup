


//current positionMain
var posMain = 0;
//number of slides
var totalSlidesMain = $('#slider-wrapMain ul li').length;
//get the slide width
var sliderWidthMain = $('#slider-wrapMain').width();


$(document).ready(function () {


	/*****************
	 BUILD THE SLIDER
	*****************/
    //set width to be 'x' times the number of slides
    $('#slider-wrapMain ul#sliderMain').width(sliderWidthMain * totalSlidesMain);

    //nextMain slide 	
    $('#nextMain').click(function () {
        slideRightMain();
    });

    //previousMain slide
    $('#previousMain').click(function () {
        slideLeftMain();
    });



	/*************************
	 //*> OPTIONAL SETTINGS
	************************/
    //automatic slider
    // delete here
    // var autoSliderMain = setInterval(slideRightMain, 3000);

    //for each slide 
    // delete here
    $.each($('#slider-wrapMain ul li'), function () {
        //set its color
        var cMain = $(this).attr("data-color");
        $(this).css("background", cMain);

        //create a paginationMain
        var liMain = document.createElement('li');
        $('#paginationMain-wrap ul').append(liMain);
    });

    //counterMain
    countSlidesMain();

    //paginationMain
    paginationMain();

    //hide/show controls/btns when hover
    //pause automatic slide when hover
    $('#slider-wrapMain').hover(
        function () { $(this).addClass('activeMain'); clearInterval(autoSliderMain); },
        // function () { $(this).removeClass('activeMain'); autoSliderMain = setInterval(slideRightMain, 3000); }
    );



});//DOCUMENT READY



/***********
 SLIDE LEFT
************/
function slideLeftMain() {
    posMain--;
    if (posMain == -1) { posMain = totalSlidesMain - 1; }
    $('#slider-wrapMain ul#sliderMain').css('left', -(sliderWidthMain * posMain));

    //*> optional
    countSlidesMain();
    paginationMain();
}


/************
 SLIDE RIGHT
*************/
function slideRightMain() {
    posMain++;
    if (posMain == totalSlidesMain) { posMain = 0; }
    $('#slider-wrapMain ul#sliderMain').css('left', -(sliderWidthMain * posMain));

    //*> optional 
    countSlidesMain();
    paginationMain();
}




/************************
 //*> OPTIONAL SETTINGS
************************/
function countSlidesMain() {
    $('#counterMain').html(posMain + 1 + ' / ' + totalSlidesMain);
}

function paginationMain() {
    $('#paginationMain-wrap ul li').removeClass('activeMain');
    $('#paginationMain-wrap ul li:eq(' + posMain + ')').addClass('activeMain');
}

