// Get the modal
var modal = document.getElementById('myModal');

// Get the main container and the body
var body = document.getElementsByTagName('body');
var container = document.getElementById('no-babbal');

// Get the open button
var btnOpen = document.getElementById("status-range");

// Get the close button
var btnClose = document.getElementById("closeModal");

// Open the modal
btnOpen.onclick = function() {
    modal.className = "Modal is-visuallyHidden";
    setTimeout(function() {
    //   container.className = "MainContainer is-blurred";
    container.classList.add("is-blurred");
      modal.className = "Modal";
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