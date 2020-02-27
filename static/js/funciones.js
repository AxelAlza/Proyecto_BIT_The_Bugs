$(document).ready(function(){
    var cedula = 0;
$("#table tr").click(function(event){
   $(this).addClass('table-primary').siblings().removeClass('table-primary');
   cedula=$(this).find('td:first').html();})

$("#eliminar").click(function(event){
    $.ajax(
              {
                    type:'POST',
                    contentType:'application/json;charset-utf-08',
                    dataType:'json',
                    url:'http://127.0.0.1:5000/pass_val?cedula='+cedula ,
                    success:function (data) {
                        var reply=data.reply;
                        if (reply=="success")
                        {
                            alert("Eliminado")
                            return;
                        }
                        else
                            {
                            alert("some error ocured in session agent")
                            }
                    }
                }
            );
})

});




