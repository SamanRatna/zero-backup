function navigationMode(){
    myKeyboard = document.getElementById("keyboard-2");
    if(myKeyboard != null){
        // document.getElementById("yatri-logo-2").style.display = "none";
        document.getElementById("status-2").style.display ="none";
        myKeyboard.style.display="block";

    }
}

function closeKeyboard(){
    console.log("Closing Keyboard");
    myKeyboard = document.getElementById("keyboard-2");
    if(myKeyboard != null){
        // document.getElementById("yatri-logo-2").style.display = "none";
        document.getElementById("status-2").style.display ="block";
        myKeyboard.style.display="none";

    }
}

function toggleKeyboard(){
    myStatus = document.getElementById("status-2");
    myLogo = document.getElementById("yatri-logo-2");
    if(toggleKeyboard.state=='closed'){
        console.log("Opening Keyboard");
        if(myKeyboard != null){
            toggleKeyboard.state = 'open';
            myStatus.style.animation ="vanishingStatus 0.5s 1 ease-out forwards";
            myLogo.style.boxShadow = "0px -4px 5px 0px rgba(219,219,219,1)";
        }
    }
    else if(toggleKeyboard.state=='open'){
        console.log("Closing Keyboard");
        if(myKeyboard != null){
            myStatus.style.animation ="appearingStatus 0.5s 1 ease-out forwards";
            myStatus.style.display ="block";
            toggleKeyboard.state = 'closed';
            myLogo.style.boxShadow = "none";
        }
    }
}

toggleKeyboard.state = 'closed';
