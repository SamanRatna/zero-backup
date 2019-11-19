function timeCount() {
    var today = new Date();
    
    const day = today.toLocaleString('en-us', { weekday: 'long' });

    var hour = today.getHours();
    if(hour<10)hour = "0"+hour;

    var minute = today.getMinutes();
    if(minute<10)minute = "0"+minute;

    document.getElementById('notification-time').innerHTML = hour + ':' + minute;
    
    setTimeout("timeCount()", 10);
}

timeCount();
