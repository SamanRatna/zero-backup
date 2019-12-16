function loadScript(url, callback){

    var script = document.createElement("script")
    script.type = "text/javascript";

    if (script.readyState){  //IE
        script.onreadystatechange = function(){
            if (script.readyState == "loaded" ||
                    script.readyState == "complete"){
                script.onreadystatechange = null;
                callback();
            }
        };
    } else {  //Others
        script.onload = function(){
            callback();
        };
    }

    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}

function reloadMap(){
    loadScript("https://maps.googleapis.com/maps/api/js?key=AIzaSyDcaohklnZiHr2YywkAJbwV9o3EAF5JVcs", initMap);
}

function reloadPage(){
    window.location.reload();
}
document.getElementById('yatri-logo').addEventListener('click', reloadMap);
document.getElementById('notification-time').addEventListener('click', reloadPage);
