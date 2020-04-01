mode = GetURLParameter("mode")

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
  if ($('#CliCi').val().toString().length != 8) {
    alert("La cedula debe ser de 8 digitos")
    return true
  }
  if ($('#CliAge').val() < 0) {
    alert("La edad no puede ser menor a 0")
    return true
  }

  return false
}

function gethospitales() {
  $.get("/Mantenimiento/gethospitales", function(data) {
    data = JSON.parse(data);
    for (var hospital of data) {
      var str = ''
      if (parseInt(hospital.hosid) == parseInt(hos)) {
        str = " selected"
      }
      $("#Hospitales").append('<option value ="' + hospital.hosid + '"' + str + '>' + hospital.hosnom + "</option>")
    }
  })
}

function getdata(ced) {
  $.get("/getdata?ced=" + ced + "&modo=cli", function(data) {
    data = JSON.parse(data);
    $('#CliCi').val(ced);
    $('#CliNom').val(data[0].clinom);
    $('#CliApe').val(data[0].cliape);
    $('#CliAge').val(data[0].cliage);
    hos = data[0].clihid
    gethospitales();
  });


};


if (mode == "UPD") {
  var ced = GetURLParameter("cedula")
  getdata(ced)
  $("#titulo").text("Modificar Cliente");
} else {
  hos = null
  gethospitales()
}



$(document).ready(function() {
  var cedula;
  var cedulabien = 'N';
  $("#CliCi").keyup(function() {
    if (parseInt(ced) != $('#CliCi').val()) {
      cedula = $(this).val();
      $.ajax({
        type: 'POST',
        contentType: 'application/json;charset-utf-08',
        dataType: 'json',
        url: '/CedulaDisponible?cedula=' + cedula + '&modo=cli',
        success: function(data) {
          var reply = data.reply;
          if (reply == "success") {
            $("#CliCi").popover('hide');
            cedulabien = 'S';
          } else {
            $("#CliCi").popover('show');
            cedulabien = 'N';
          }
        }
      })
    }
  })

  $("#send").submit(function(event) {
    if (mode == "INS") {
      if (cedulabien != 'S' || ValidateForm()) {
        event.preventDefault();
      }
    }
  })
})
