$("#table tr").click(function(){
   $(this).addClass('table-primary').siblings().removeClass('table-primary');
   var value=$(this).find('td:last').html();
});

