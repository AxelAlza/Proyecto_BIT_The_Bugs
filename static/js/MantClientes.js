$(document).ready(function() {
    var cedula
    var $table = $('#table')
    var $button = $('#table')
    $(function() {
        $button.click(function() {
            var json = $table.bootstrapTable('getSelections')
            for (i in json) {
                 cedula = json[i].empci;
                }
        })
    })
    $("#eliminar").click(function() {
        if (cedula == undefined) {
            alert("Debe seleccionar un cliente de la lista")
        } else {
            $.ajax({
                type: 'POST',
                contentType: 'application/json;charset-utf-08',
                dataType: 'json',
                url: '/EliminarCliente?cedula=' + cedula,
                success: function(data) {
                    var reply = data.reply;
                    if (reply == "success") {
                        location.reload(true)
                        alert("Elminado")
                    } else {
                        alert("Ha ocurrido un error")
                    }
                }
            })
        }
    })
})
