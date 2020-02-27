$("#table tr").click(function(){
   $(this).addClass('table-primary').siblings().removeClass('table-primary');
   var cedula=$(this).find('td:first').html();
});



