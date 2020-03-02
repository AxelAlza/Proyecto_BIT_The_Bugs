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

  if ($('#EmpAge').val() < 18) {
    alert("La edad no puede ser menor a 18")
    return true
  }
  if ($("#EmpHde").val() > 23 || $("#EmpHde").val() < 0) {
    alert("Eliga una hora valida")
    return true
  }
  if (($("#EmpHha").val() > 23 || $("#Emphha").val() < 0)) {
    alert("Eliga una hora valida")
    return true
  }
  if ($("#EmpHde").val() < $("#Emphha").val()) {
    alert("La hora hasta no debe ser menor a la inicial")
    return true
  }
  return false
}

function getdata(ced) {
  $.get("/getdataemp?ced=" + ced + "&modo=emp", function(data) {
    data = JSON.parse(data);
    $('#EmpCi').val(ced);
    $('#EmpNom').val(data[0].empnom);
    $('#EmpApe').val(data[0].empape);
    $('#EmpAge').val(data[0].empage);
    $("#EmpTel").val(data[0].emptel);
    $("#EmpDir").val(data[0].empdir);
    $("#EmpMail").val(data[0].empmail);
    $("#EmpHde").val(data[0].emphde);
    $("#EmpHha").val(data[0].emphha);
  });
}

var mode = GetURLParameter("mode")

if (mode == "UPD") {
  var ced = GetURLParameter("cedula")
  getdata(ced)
}

$(document).ready(function() {
  var cedula;
  var largobien = 'N';
  var cedulabien = 'N';
  $("#EmpCi").keyup(function() {
    cedula = $(this).val();
    if ($(this).val().toString().length == 8) {
      largobien = 'S';
      $.ajax({
        type: 'POST',
        contentType: 'application/json;charset-utf-08',
        dataType: 'json',
        url: '/CedulaDisponibleEmp?cedula=' + cedula + '&modo=emp',
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
    } else {
      largobien = 'N'
    }
  })
  $("#send").submit(function(event) {
    if (mode == "INS") {
      if (largobien != 'S' || cedulabien != 'S' || ValidateForm()) {
        event.preventDefault();
      } else {
        window.location.replace('/Mantenimiento/Empleados');
      }
    }
  })
})
