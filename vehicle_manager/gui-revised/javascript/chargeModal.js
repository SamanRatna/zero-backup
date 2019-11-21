var modal;
// Get the socModal
var chargeModal = document.getElementById('fastChargeModal');
// Get the main container and the body
var body = document.getElementsByTagName('body');
var container = document.getElementById('page-one');

// Open button for SOC/Range
var chargeOpen = document.getElementById("fast-charge");

// Get the close button
var btnClose = document.getElementById("closeModal");

// Open the SOC modal
chargeOpen.onclick = function() {
    modal=chargeModal;
    chargeModal.className = "Modal is-visuallyHidden";
    setTimeout(function() {
    //   container.className = "MainContainer is-blurred";
    container.classList.add("is-blurred");
    chargeModal.className = "Modal";
    }, 100);
    container.parentElement.className = "ModalOpen";
    
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