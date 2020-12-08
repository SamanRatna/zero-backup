const swupdateStates = {
    NONE        :   'none',
    AVAILABLE   :   'available',
    DOWNLOADING :   'downloading',
    DOWNLOADED  :   'downloaded',
    INSTALLING  :   'installing',
    INSTALLED   :   'installed',
    SUCCESS     :   'success',
    FAILED      :   'failed'
}

let supdateState = swupdateStates.NONE;


function requestSWUpdateConfirmation(update_info){
    console.log(update_info)
    document.getElementById('js-swupdate-msg').innerHTML = update_info;
    setSWUpdateNotificationVisibility(true);
}
// dictionary that will contain values as response from UI to python backend
let swupdateResponse_dict = {};
swupdateResponse_dict = {
    "update_apply": null,
    "update_check": null
};
// When user chooses to install the update
document.getElementById('js-swupdate-install').addEventListener('click', function(){
    // close the notification pop-up after user clicks 'Install'
    setSWUpdateNotificationVisibility(false);
    // send exit status 0 for proceeding to update installation
    swupdateResponse_dict["update_apply"] = 0;
    // Send the exit status to gui.py
    eel.swupdateResponse(swupdateResponse_dict["update_apply"]);
})
// when user chooses to check for update
document.getElementById('js-swupdate-check').addEventListener('click', function(){
    // close the notification pop-up after user clicks 'Check for update'
    setSWUpdateNotificationVisibility(false);
    // send 'check' request message to gui.py
    swupdateResponse_dict["update_check"] = "check";
    eel.swupdateResponse(swupdateResponse_dict["update_check"]);
})
document.getElementById('js-swupdate-cancel').addEventListener('click', function(){
    setSWUpdateNotificationVisibility(false);
    swupdateResponse_dict["update_apply"] = 1;
    eel.swupdateResponse(swupdateResponse_dict["update_apply"]);
})