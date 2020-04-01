var $Hde = $('#lmao')
var $Hha = $('#lmao2')
var $hora = $("#hora")
var key = "";
var destino = "";
var destinoPro = "";
var empci;

function validarhora() {
    var Hde = /^([0-1][0-9]|2[0-3]):([0-5][0-9])$/.test($Hde.val());
    var Hha = /^([0-1][0-9]|2[0-3]):([0-5][0-9])$/.test($Hha.val());
    if (Hde || Hha) {
        return false
    } else
        return true
}

function getEmpleadoDisponible() {
    $.get("/getapikey", function(data) {
        key = data
    })

    cedula = GetURLParameter("cedula")
    var dest = new Promise(function(resolve, reject) {
        $.get("/gethos?ced=" + cedula, function(data) {
            destino = data.toString()
            destinoPro = destino.replace(/ /g, '+');
            resolve(destinoPro)
        })
    })
    dest.then(function(value) {
        $.get("/getoptemp?Destino=" + value + "&EmpHde=" + $Hde.val() + "&EmpHha=" + $Hha.val(), function(emps) {
            empleados = JSON.parse(emps)
            i = 0
            for (var empleado of empleados) {
                origen = empleado.empbarrio + " " + empleado.empcalle + " " + empleado.empnro
                origenPro = origen.replace(/ /g, '+');
                id = empleado.empci.substring(0, 8)
                $myString = $('<a class="list-group-item list-group-item-action" value ="' + id + '" id="emp' + i + '" data-toggle="list" href="#empcon' + i + '" role="tab" aria-controls="emp' + i + '">' + empleado.empci + '</a>')
                $($myString).appendTo("#tabs").find('a').click(function() {
                    alert(this.val())
                })
                $("#tabcontent").append('<div class="tab-pane fade" id="empcon' + i + '" role="tabpanel"><p>Telefono: ' + empleado.emptel + ', Desde: ' + origen + ' ' + 'Hasta: ' + destino + " Son " + empleado.distext + " y se demoran en llegar " + empleado.duration + ' Aprox.' + '</p>' +
                    '<iframe width="600" height="450" frameborder="0" style="border:0"src="https://www.google.com/maps/embed/v1/directions?mode=transit&origin=' + origenPro + '&destination=' + destinoPro + '&key=' + key + '"' + 'allowfullscreen></iframe>' + '</div>')
                i++
            }
        })
    })
}

function GetURLParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

$(function() {
    ced = GetURLParameter("cedula")
    fch = GetURLParameter("fecha")
    $.get("/getdata?ced=" + ced + "&fch=" + fch, function(data) {
        data = JSON.parse(data);
        $('#fecha').val(data[0].turfch);
        $('#cliente').val(data[0].clici);
        $('#hospital').val(data[0].clihid);
    })
})

$(document).ready(function() {
    $hora.click(function() {
        switch (parseInt($hora.val())) {
            case 0:
                $Hde.val("")
                $Hha.val("")
                $("#HoraPers").hide();
            case 1:
                $Hde.val("06:00")
                $Hha.val("14:00")
                $("#HoraPers").hide();
                break;
            case 2:
                $Hde.val("14:00")
                $Hha.val("22:00")
                $("#HoraPers").hide();
                break;
            case 3:
                $Hde.val("22:00")
                $Hha.val("06:00")
                $("#HoraPers").hide();
                break;
            case 4:
                $Hde.val("")
                $Hha.val("")
                $("#HoraPers").show();
                break;
            default:
                $("#HoraPers").hide();
                break;
        }
    })

    $("#ConfirmarHorario").click(function() {
        if (validarhora()) {
            alert("Debe proporcionar una hora valida")
        } else {
            getEmpleadoDisponible()
            $hora.prop("readonly", true)
            $Hde.prop("readonly", true)
            $Hha.prop("readonly", true)
            $('#Empleados').collapse()
            $("#ConfirmarHorario").prop("disabled", true);
            console.log($Hde.val())
            console.log($Hha.val())
        }
    })
})

$("#Confirmar").click(function(event) {
    id = ($("#tabs").children(".active").text())
    $("#id").val(id.substring(0,8))
    if (id == undefined || $("#id").val().length != 8){
      alert("seleccione un empleado de la lista")
      event.preventDefault();
    }
})
