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
    myKeyboard = document.getElementById("keyboard-2");
    myForm = document.getElementById("navigation-form-1");
    if(toggleKeyboard.state=='closed'){
        console.log("Opening Keyboard");
        if(myKeyboard != null){
            document.getElementById("status-2").style.display ="none";
            myKeyboard.style.display="block";
            myForm.style.display ="block";
            toggleKeyboard.state = 'open';
        }
    }
    else if(toggleKeyboard.state=='open'){
        console.log("Closing Keyboard");
        if(myKeyboard != null){
            document.getElementById("status-2").style.display ="block";
            myForm.style.display ="none";
            myKeyboard.style.display="none";
            toggleKeyboard.state = 'closed';
        }
    }
}

toggleKeyboard.state = 'closed';

function openSearchDialog(){
    // Get the modal
    var modal = document.getElementById("search-mode-1");

    // Get the button that opens the modal
    var btn = document.getElementById("nav-button");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal 
    btn.onclick = function() {
      modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
}

// function longPressNavigate(){
//     var region = document.getElementById('yatri-logo-1');

//     region.addEventListener('long-press', function(){
//         console.log("Long Press Detected")
//         myKeyboard = document.getElementById("keyboard-2");
//         if(myKeyboard != null){
//             document.getElementById("status-2").style.display ="none";
//             myKeyboard.style.display="block";
//         }
//     });
// }
