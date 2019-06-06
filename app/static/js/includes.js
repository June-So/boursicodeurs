/* Prediction */
$('#btn-load-instruments').click(function(){
console.log('ranafoot');
    $('#instruments-fxcm').html('<p>Chargement des instruments depuis la plateforme FXCM...</p>');
    $.ajax({
        url : '/load-instruments',
        success : function(html){
            $('#instruments-fxcm').html(html);
        }
    });
});