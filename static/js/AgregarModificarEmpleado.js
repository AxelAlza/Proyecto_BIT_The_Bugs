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
function ValidateForm() {
  if ($('#EmpCi').val().toString().length != 8) {
    alert("La cedula debe ser de 8 digitos")
    return true
  }
  if ($('#EmpAge').val() < 18) {
    alert("La edad no puede ser menor a 18")
    return true
  }
  return false
}
function getdata(ced) {
  $.get("/getdata?ced=" + ced + "&modo=emp", function(data) {
    data = JSON.parse(data);
    $('#EmpCi').val(ced);
    $('#EmpNom').val(data[0].empnom);
    $('#EmpApe').val(data[0].empape);
    $('#EmpAge').val(data[0].empage);
    $("#EmpTel").val(data[0].emptel);
    $("#EmpBarrio").val(data[0].empbarrio);
    $("#EmpCalle").val(data[0].empcalle);
    $("#EmpNro").val(data[0].empnro);
    $("#EmpMail").val(data[0].empmail);
    $("#EmpHde").val(data[0].emphde);
    $("#EmpHha").val(data[0].emphha);
  });
}

var mode = GetURLParameter("mode")

if (mode == "UPD") {
  var ced = GetURLParameter("cedula")
  getdata(ced)
  $("#titulo").text("Modificar Empleado");
}

$(document).ready(function() {

  var cedula
  var cedulabien = 'N';
  $("#EmpCi").keyup(function() {
    if (parseInt(ced) != $('#EmpCi').val()) {
      cedula = $(this).val();
      $.ajax({
        type: 'POST',
        contentType: 'application/json;charset-utf-08',
        dataType: 'json',
        url: '/CedulaDisponible?cedula=' + cedula + '&modo=emp',
        success: function(data) {
          var reply = data.reply;
          if (reply == "success") {
            $("#EmpCi").popover('hide');
            cedulabien = 'S';
          } else {
            $("#EmpCi").popover('show');
            cedulabien = 'N';
          }
        }
      })
    }
  })

  $("#send").submit(function(event) {
    if (mode == "INS") {
      if  (cedulabien != 'S' || ValidateForm()) {
        event.preventDefault();
      }
    }
  })
})
