$(document).ready(function () {
    //speed button	
    $('#infograph-btn-speed').click(function () {
        $('#temperature-infograph').css('display','block');
        $('#speed-infograph').css('display','none');

    });
    $('#infograph-btn-temperature').click(function () {
        $('#carbon-infograph').css('display','block');
        $('#temperature-infograph').css('display','none');

    });
    $('#infograph-btn-carbon').click(function () {
        $('#speed-infograph').css('display','block');
        $('#carbon-infograph').css('display','none');

    });
});//DOCUMENT READY