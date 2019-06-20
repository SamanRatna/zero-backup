var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("demo");
    // var captionText = document.getElementById("caption");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    // dots[slideIndex-1].className += " active";
    // captionText.innerHTML = dots[slideIndex-1].alt;
}




// ride_mode = 1
// setInterval(function(){
//     if(ride_mode == 1){
//         ride_mode = 2
//     } else {
//         ride_mode = 1
//     }
//     console.log(ride_mode)
//     console.log(pos)

//     if (ride_mode == 2) {
//         plusSlides(1);
//         logstuff()
//     }
// }, 5000)

/*












above this - Mainslider

now - SLider














*/

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
    $('#next').click(function () {
        slideRight();
    });

    //previous slide
    $('#previous').click(function () {
        slideLeft();
    });



	/*************************
	 //*> OPTIONAL SETTINGS
	************************/
    //automatic slider
    // delete here
    // var autoSlider = setInterval(slideRight, 3000);

    //for each slide
    // delete here
    $.each($('#slider-wrap ul li'), function () {
        //set its color
        var c = $(this).attr("data-color");
        $(this).css("background", c);

        //create a pagination
        var li = document.createElement('li');
        $('#pagination-wrap ul').append(li);
    });

    //counter
    countSlides();

    //pagination
    pagination();

    //hide/show controls/btns when hover
    //pause automatic slide when hover
    $('#slider-wrap').hover(
        function () { $(this).addClass('active'); clearInterval(autoSlider); },
        // function () { $(this).removeClass('active'); autoSlider = setInterval(slideRight, 3000); }
    );



});//DOCUMENT READY



/***********
 SLIDE LEFT
************/
function slideLeft() {
    pos--;
    if (pos == -1) { pos = totalSlides - 1; }
    $('#slider-wrap ul#slider').css('left', -(sliderWidth * pos));

    //*> optional
    countSlides();
    pagination();
}


/************
 SLIDE RIGHT
*************/
function slideRight() {
    pos++;
    if (pos == totalSlides) { pos = 0; }
    $('#slider-wrap ul#slider').css('left', -(sliderWidth * pos));

    //*> optional
    countSlides();
    pagination();
}




/************************
 //*> OPTIONAL SETTINGS
************************/
function countSlides() {
    $('#counter').html(pos + 1 + ' / ' + totalSlides);
}

function pagination() {
    $('#pagination-wrap ul li').removeClass('active');
    $('#pagination-wrap ul li:eq(' + pos + ')').addClass('active');
}

/*












above this - slider

now - music














*/
// Mythium Archive: https://archive.org/details/mythium/


jQuery(function ($) {
    'use strict'
    var supportsAudio = !!document.createElement('audio').canPlayType;
    if (supportsAudio) {
        // initialize plyr
        var player = new Plyr('#audio1', {
            controls: [
                'restart',
                'play',
                'progress',
                'current-time',
                'duration',
                'mute',
                'volume'
            ]
        });
        // initialize playlist and controls
        var index = 0,
            playing = false,
            mediaPath = '{{ url_for('static', filename='music/')}}',
            extension = '',
            tracks = [{
                "track": 1,
                "name": "All This Is - Joe L.'s Studio",
                "duration": "2:46",
                "file": "JLS_ATI"
            }, {
                "track": 2,
                "name": "The Forsaken - Broadwing Studio (Final Mix)",
                "duration": "8:30",
                "file": "BS_TF"
            }, {
                "track": 3,
                "name": "All The King's Men - Broadwing Studio (Final Mix)",
                "duration": "5:01",
                "file": "BS_ATKM"
            }, {
                "track": 4,
                "name": "The Forsaken - Broadwing Studio (First Mix)",
                "duration": "8:31",
                "file": "BSFM_TF"
            }, {
                "track": 5,
                "name": "All The King's Men - Broadwing Studio (First Mix)",
                "duration": "5:05",
                "file": "BSFM_ATKM"
            }, {
                "track": 6,
                "name": "All This Is - Alternate Cuts",
                "duration": "2:48",
                "file": "AC_ATI"
            }, {
                "track": 7,
                "name": "All The King's Men (Take 1) - Alternate Cuts",
                "duration": "5:44",
                "file": "AC_ATKMTake_1"
            }, {
                "track": 8,
                "name": "All The King's Men (Take 2) - Alternate Cuts",
                "duration": "5:26",
                "file": "AC_ATKMTake_2"
            }, {
                "track": 9,
                "name": "Magus - Alternate Cuts",
                "duration": "5:46",
                "file": "AC_M"
            }, {
                "track": 10,
                "name": "The State Of Wearing Address (fucked up) - Alternate Cuts",
                "duration": "5:25",
                //     "file": "AC_TSOWAfucked_up"
                // }, {
                //     "track": 11,
                //     "name": "Magus - Popeye's (New Years '04 - '05)",
                //     "duration": "5:53",
                //     "file": "PNY04-05_M"
                // }, {
                //     "track": 12,
                //     "name": "On The Waterfront - Popeye's (New Years '04 - '05)",
                //     "duration": "4:40",
                //     "file": "PNY04-05_OTW"
                // }, {
                //     "track": 13,
                //     "name": "Trance - Popeye's (New Years '04 - '05)",
                //     "duration": "13:15",
                //     "file": "PNY04-05_T"
                // }, {
                //     "track": 14,
                //     "name": "The Forsaken - Popeye's (New Years '04 - '05)",
                //     "duration": "8:12",
                //     "file": "PNY04-05_TF"
                // }, {
                //     "track": 15,
                //     "name": "The State Of Wearing Address - Popeye's (New Years '04 - '05)",
                //     "duration": "7:02",
                //     "file": "PNY04-05_TSOWA"
                // }, {
                //     "track": 16,
                //     "name": "Magus - Popeye's (Valentine's Day '05)",
                //     "duration": "5:43",
                //     "file": "PVD_M"
                // }, {
                //     "track": 17,
                //     "name": "Trance - Popeye's (Valentine's Day '05)",
                //     "duration": "10:45",
                //     "file": "PVD_T"
                // }, {
                //     "track": 18,
                //     "name": "The State Of Wearing Address - Popeye's (Valentine's Day '05)",
                //     "duration": "5:36",
                //     "file": "PVD_TSOWA"
                // }, {
                //     "track": 19,
                //     "name": "All This Is - Smith St. Basement (01/08/04)",
                //     "duration": "2:48",
                //     "file": "SSB01_08_04_ATI"
                // }, {
                //     "track": 20,
                //     "name": "Magus - Smith St. Basement (01/08/04)",
                //     "duration": "5:46",
                //     "file": "SSB01_08_04_M"
                // }, {
                //     "track": 21,
                //     "name": "Beneath The Painted Eye - Smith St. Basement (06/06/03)",
                //     "duration": "13:07",
                //     "file": "SSB06_06_03_BTPE"
                // }, {
                //     "track": 22,
                //     "name": "Innocence - Smith St. Basement (06/06/03)",
                //     "duration": "5:16",
                //     "file": "SSB06_06_03_I"
                // }, {
                //     "track": 23,
                //     "name": "Magus - Smith St. Basement (06/06/03)",
                //     "duration": "5:46",
                //     "file": "SSB06_06_03_M"
                // }, {
                //     "track": 24,
                //     "name": "Madness Explored - Smith St. Basement (06/06/03)",
                //     "duration": "4:51",
                //     "file": "SSB06_06_03_ME"
                // }, {
                //     "track": 25,
                //     "name": "The Forsaken - Smith St. Basement (06/06/03)",
                //     "duration": "8:43",
                //     "file": "SSB06_06_03_TF"
                // }, {
                //     "track": 26,
                //     "name": "All This Is - Smith St. Basement (12/28/03)",
                //     "duration": "3:00",
                //     "file": "SSB12_28_03_ATI"
                // }, {
                //     "track": 27,
                //     "name": "Magus - Smith St. Basement (12/28/03)",
                //     "duration": "6:09",
                //     "file": "SSB12_28_03_M"
                // }, {
                //     "track": 28,
                //     "name": "Madness Explored - Smith St. Basement (12/28/03)",
                //     "duration": "5:05",
                //     "file": "SSB12_28_03_ME"
                // }, {
                //     "track": 29,
                //     "name": "Trance - Smith St. Basement (12/28/03)",
                //     "duration": "12:32",
                //     "file": "SSB12_28_03_T"
                // }, {
                //     "track": 30,
                //     "name": "The Forsaken - Smith St. Basement (12/28/03)",
                //     "duration": "8:56",
                //     "file": "SSB12_28_03_TF"
                // }, {
                //     "track": 31,
                //     "name": "All This Is (Take 1) - Smith St. Basement (Nov. '03)",
                //     "duration": "4:55",
                //     "file": "SSB___11_03_ATITake_1"
                // }, {
                //     "track": 32,
                //     "name": "All This Is (Take 2) - Smith St. Basement (Nov. '03)",
                //     "duration": "5:45",
                //     "file": "SSB___11_03_ATITake_2"
                // }, {
                //     "track": 33,
                //     "name": "Beneath The Painted Eye (Take 1) - Smith St. Basement (Nov. '03)",
                //     "duration": "14:05",
                //     "file": "SSB___11_03_BTPETake_1"
                // }, {
                //     "track": 34,
                //     "name": "Beneath The Painted Eye (Take 2) - Smith St. Basement (Nov. '03)",
                //     "duration": "13:25",
                //     "file": "SSB___11_03_BTPETake_2"
                // }, {
                //     "track": 35,
                //     "name": "The Forsaken (Take 1) - Smith St. Basement (Nov. '03)",
                //     "duration": "8:37",
                //     "file": "SSB___11_03_TFTake_1"
                // }, {
                //     "track": 36,
                //     "name": "The Forsaken (Take 2) - Smith St. Basement (Nov. '03)",
                //     "duration": "8:36",
                "file": "SSB___11_03_TFTake_2",
            }],
            buildPlaylist = $(tracks).each(function (key, value) {
                var trackNumber = value.track,
                    trackName = value.name,
                    trackDuration = value.duration;
                if (trackNumber.toString().length === 1) {
                    trackNumber = '0' + trackNumber;
                }
                $('#plList').append('<li> \
                    <div class="plItem"> \
                        <span class="plNum">' + trackNumber + '.</span> \
                        <span class="plTitle">' + trackName + '</span> \
                        <span class="plLength">' + trackDuration + '</span> \
                    </div> \
                </li>');
            }),
            trackCount = tracks.length,
            npAction = $('#npAction'),
            npTitle = $('#npTitle'),
            audio = $('#audio1').on('play', function () {
                playing = true;
                npAction.text('Now Playing...');
            }).on('pause', function () {
                playing = false;
                npAction.text('Paused...');
            }).on('ended', function () {
                npAction.text('Paused...');
                if ((index + 1) < trackCount) {
                    index++;
                    loadTrack(index);
                    audio.play();
                } else {
                    audio.pause();
                    index = 0;
                    loadTrack(index);
                }
            }).get(0),
            btnPrev = $('#btnPrev').on('click', function () {
                if ((index - 1) > -1) {
                    index--;
                    loadTrack(index);
                    if (playing) {
                        audio.play();
                    }
                } else {
                    audio.pause();
                    index = 0;
                    loadTrack(index);
                }
            }),
            btnNext = $('#btnNext').on('click', function () {
                if ((index + 1) < trackCount) {
                    index++;
                    loadTrack(index);
                    if (playing) {
                        audio.play();
                    }
                } else {
                    audio.pause();
                    index = 0;
                    loadTrack(index);
                }
            }),
            li = $('#plList li').on('click', function () {
                var id = parseInt($(this).index());
                if (id !== index) {
                    playTrack(id);
                }
            }),
            loadTrack = function (id) {
                $('.plSel').removeClass('plSel');
                $('#plList li:eq(' + id + ')').addClass('plSel');
                npTitle.text(tracks[id].name);
                index = id;
                audio.src = mediaPath + tracks[id].file + extension;
                document.getElementsByClassName("albumArt")[0].src = mediaPath + tracks[id].file + '.png';
            },
            playTrack = function (id) {
                loadTrack(id);
                audio.play();
            };
        extension = audio.canPlayType('audio/mpeg') ? '.mp3' : audio.canPlayType('audio/ogg') ? '.ogg' : '';
        loadTrack(index);
    } else {
        // boo hoo
        $('.column').addClass('hidden');
        var noSupport = $('#audio1').text();
        $('.container').append('<p class="no-support">' + noSupport + '</p>');
    }
});



/*







above this - music

now - topBar









*/


timeCount();
function timeCount() {
    var today = new Date();

    // var day = today.getDay();        /* generates 0-6 */
    const day = today.toLocaleString('en-us', { weekday: 'long' });
    var date = today.getDate();
    // var month = today.getMonth()+1;  /* generates 0-11 */
    const month = today.toLocaleString('en-us', { month: 'long' });
    var year = today.getFullYear();

    var hour = today.getHours();
    if (hour < 10) hour = "0" + hour;

    var minute = today.getMinutes();
    if (minute < 10) minute = "0" + minute;

    var second = today.getSeconds();
    if (second < 10) second = "0" + second;

    // document.getElementById("clock").innerHTML =
    // day+"/"+month+"/"+year+" |"+hour+":"+minute+":"+second;

    document.getElementsByClassName("time")[0].innerHTML =
        hour + ":" + minute + ":" + second;
    // document.getElementsByClassName("time")[1].innerHTML =
    // hour+":"+minute+":"+second;
    // document.querySelectorAll(".time").innerHTML=hour+":"+minute+":"+second;

    // document.getElementById("time").innerHTML =
    // hour+":"+minute+":"+second;

    document.getElementsByClassName("date")[0].innerHTML =
        day + "," + date + " " + month + " " + year;

    setTimeout("timeCount()", 10);
}




/*







above this - slider

now - speed









*/
var leftTurn;

var rightTurn;


setInterval(function () {
    document.getElementsByClassName("speed")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("speedMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("powerMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("rangeMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("tripMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    // document.getElementsByClassName("lightMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);
    document.getElementsByClassName("odoMain")[0].innerHTML = Math.floor((Math.random() * 100) + 1);

    leftTurn = Math.round(Math.random());
    rightTurn = Math.round(Math.random());
    highBeamValue = Math.round(Math.random());
    modeValue = Math.round(Math.random() * 2 + 1);
    // while (leftTurn == 1) {
    // console.log(1);
    // document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOn.png";
    // setInterval(800);
    // document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOff.png";
    // setInterval(800);
    // }


    function leftTurnOnLoop() {
        setTimeout(function () {
            if (leftTurn == 1) {
                document.getElementsByClassName("leftTurn")[0].src = "{{ url_for('static', filename='images/leftArrowOn.png')}}";
                leftTurnOffLoop();
            }
        }, 300)
    }


    function leftTurnOffLoop() {
        setTimeout(function () {
            document.getElementsByClassName("leftTurn")[0].src = "{{ url_for('static', filename='images/leftArrowOff.png')}}";
            if (leftTurn == 1) {
                leftTurnOnLoop();
            }
        }, 300)
    }


    function rightTurnOnLoop() {
        setTimeout(function () {
            if (rightTurn == 1) {
                document.getElementsByClassName("rightTurn")[0].src = "{{ url_for('static', filename='images/rightArrowOn.png')}}";
                rightTurnOffLoop();
            }
        }, 300)
    }


    function rightTurnOffLoop() {
        setTimeout(function () {
            document.getElementsByClassName("rightTurn")[0].src = "{{ url_for('static', filename='images/rightArrowOff.png')}}";
            if (rightTurn == 1) {
                rightTurnOnLoop();
            }
        }, 300)
    }

    function highBeam() {
        if (highBeamValue == 0) {
            document.getElementsByClassName("beam")[0].src = "{{ url_for('static', filename='images/rightArrowOff.png')}}highBeamOff.png";
        }
        else {
            document.getElementsByClassName("beam")[0].src = "{{ url_for('static', filename='images/highBeamOn.png')}}";
        }
    }
    if (modeValue == 1) {
        document.getElementsByClassName("modeMain")[0].src = "{{ url_for('static', filename='images/mode1.png')}}";
    } else if (modeValue == 2) {
        document.getElementsByClassName("modeMain")[0].src = "{{ url_for('static', filename='images/mode2.png')}}";
    }
    else {
        document.getElementsByClassName("modeMain")[0].src = "{{ url_for('static', filename='images/mode3.png')}}";
    }


    leftTurnOffLoop();
    leftTurnOnLoop();
    rightTurnOffLoop();
    rightTurnOnLoop();
    highBeam();


    //     setInterval(100);
    //     document.getElementsByClassName("leftTurn")[0].src = "files/images/leftArrowOff.png";
    //     setInterval(100);



    // console.log(leftTurn=Math.round(Math.random()));
    // rightTurn=Math.round(Math.random());
    // document.getElementsByClassName("leftTurn")[0].src== "files/images/leftArrowOn.png";
}, 1500);

// console.log(leftTurn=Math.round(Math.random()));


// setInterval(function(){
//     leftTurn=Math.round(Math.random());
//     rightTurn=Math.round(Math.random());
// }, 1000);
