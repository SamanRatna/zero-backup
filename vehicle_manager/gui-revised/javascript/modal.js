var modal;
// Get the socModal
var socModal = document.getElementById('range2-modal');
// var tripResetModal = document.getElementById("tripResetModal");
var naviModal = document.getElementById("navigation-modal");
// Get the main container and the body
var body = document.getElementsByTagName('body');
var container = document.getElementById('page-zero');

// Open button for SOC/Range
var socOpen = document.getElementById("soc-status");

// Open button for trip reset
// var tripResetOpen = document.getElementById("infocard-trips");

// Open button for keyboard modal
var naviOpen = document.getElementById("navigation-button");

// Get the close button
var btnClose = document.getElementById("closeModal");

// Open the SOC modal
socOpen.onclick = function() {
    modal=socModal;
    socModal.className = "Modal is-visuallyHidden";
    setTimeout(function() {
    //   container.className = "MainContainer is-blurred";
    container.classList.add("is-blurred");
      socModal.className = "Modal";
    }, 100);
    container.parentElement.className = "ModalOpen";
    setTimeout(function(){
        console.log('Closing the modal.')
        closeModal();
    }, 3000);
}

// Open the reset trip modal
// tripResetOpen.onclick = function() {
// function openTripResetModal(){
//     modal = tripResetModal;
//     tripResetModal.className = "Modal is-visuallyHidden";
//     setTimeout(function() {
//     //   container.className = "MainContainer is-blurred";
//     container.classList.add("is-blurred");
//       tripResetModal.className = "Modal";
//     }, 100);
//     container.parentElement.className = "ModalOpen";
// }

// Open the SOC modal
naviOpen.onclick = function() {
    modal=naviModal;
    naviModal.className = "Modal is-visuallyHidden";
    setTimeout(function() {
    //   container.className = "MainContainer is-blurred";
    // container.classList.add("is-blurred");
    naviModal.className = "Modal";
    }, 100);
    container.parentElement.className = "ModalOpen";
    setTimeout(function(){
        console.log('Closing the modal.')
        closeModal();
    }, 2000);
}
// Close the modal
btnClose.onclick = function() {
    modal.className = "Modal is-hidden is-visuallyHidden";
    body.className = "";
    container.classList.remove("is-blurred");
    // container.parentElement.className = "";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.className = "Modal is-hidden";
        body.className = "";
        container.classList.remove("is-blurred");
        // container.parentElement.className = "";
    }
}

function closeModal() {
    modal.className = "Modal is-hidden is-visuallyHidden";
    body.className = "";
    container.classList.remove("is-blurred");
    // container.parentElement.className = "";
}

// function openKeyboardModal(){
//     modal = keyboardModal;
//     keyboardModal.className = "Modal is-visuallyHidden";
//     setTimeout(function() {
//     //   container.className = "MainContainer is-blurred";
//     // container.classList.add("is-blurred");
//       keyboardModal.className = "Modal";
//     }, 100);
//     container.parentElement.className = "ModalOpen";
//     setTimeout(function(){
//         console.log('Closing the modal.')
//         closeModal();
//     }, 2000);
// }