var $table = $('#table')
var $ok = $('#ok')
var cedula
var fecha
function filter(Row, Filters) {
  if (Row.turfch != $("#fecha").val()) {
    return false
  }
  else {
    if (parseInt($("#estado").val()) == 1) {
      return true
    } else if (parseInt($("#estado").val()) == 2 && Row.empci == "None") {
      return true
    } else if (parseInt($("#estado").val()) == 3 && Row.empci != "None") {
      return true
    } else {
      return false
    }
  }
}
$(document).ready(function() {

  $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['es-UY'])

  Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
  });

  document.getElementById('fecha').value = new Date().toDateInputValue();

  $(function() {
    $table.bootstrapTable('filterBy', {
      turfch: $("#fecha").val()
    })})

    $("#table").click(function() {
      var json = $table.bootstrapTable('getSelections')
      fecha = json[0].turfch
      str = json[0].clici.toString()
      cedula = str.substring(0,8)
    })

    $(function() {
      $("#ok").click(function() {
        $table.bootstrapTable('filterBy', {
          empci: $("#estado").val(),
          turfch: $("#fecha").val()
        }, {
            'filterAlgorithm': filter
          })
      })
    })
    $("#Asignar").click(function() {
      if (cedula == undefined || fecha == undefined) {
        event.preventDefault();
        alert("Debe seleccionar un turno de la lista")
      }
      else {
        window.location.replace("/Asignar?cedula="+cedula+"&fecha="+fecha);
      }
    })
  })
