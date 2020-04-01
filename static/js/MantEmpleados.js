  $(document).ready(function() {
    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['es-UY'])
    var cedula
    var $table = $('#table')
    var $button = $('#table')
    $(function() {
        $button.click(function() {
            var json = $table.bootstrapTable('getSelections')
                 cedula = json[0].empci;
        })
    })

    $("#agregar").click(function() {
      window.location.replace("/Mantenimiento/Empleados/AgregarModificarEmpleado?mode=INS");
    } )

    $("#modificar").click(function(event) {
        if (cedula == undefined) {
            event.preventDefault();
            alert("Debe seleccionar un empleado de la lista")}
        else {
          window.location.replace("/Mantenimiento/Empleados/AgregarModificarEmpleado?mode=UPD&cedula=" + cedula);
        }
        })

    $("#eliminar").click(function() {
        if (cedula == undefined) {
            alert("Debe seleccionar un empleado de la lista")
        } else {
            $.ajax({
                type: 'POST',
                contentType: 'application/json;charset-utf-08',
                dataType: 'json',
                url: '/EliminarEmpleado?cedula=' + cedula,
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
