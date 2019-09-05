eel.expose(updateBikeMode);
function updateBikeMode(arg) {
    console.log(arg + ' from main');
    mylogo = document.getElementById('logo');

    if(arg == "MODE_STANDBY"){
        mylogo.src="files/images/logo_standby.png";
    }
    else if(arg == "MODE_SUSTE"){
        mylogo.src="files/images/logo_suste.png";
    }
    else if(arg == "MODE_THIKKA"){
        mylogo.src="files/images/logo_thikka.png";
    }
    else if(arg == "MODE_BABBAL"){
        mylogo.src="files/images/logo_babbal.png";
    }
    else if(arg == "MODE_CHARGING"){
        mylogo.src="files/images/logo_reverse.png";
    }
}
