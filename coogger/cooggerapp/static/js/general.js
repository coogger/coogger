$(document).ready(function() {
  // her zaman çalışacak kodlar
  $(".close-ms").click(function() {
    $(".main-messages").remove();
  })
  $(".b-edit-point").click(function() {
    var data_edit_id = this.getAttribute("data-edit-id");
    $(".data-edit-id-" + data_edit_id).toggle("fast");
  });
  $(".lists").click(function(){
    $("nav").toggle("fast");
  });

  $(".report").click(function(event){
    var content_id = this.getAttribute("data-content-id");
    $("body").load("/web/report/?content_id="+content_id);
  });

$( ".fa-arrow-down" ).click(function() {
  $( ".open_header_menu" ).toggle( "fast", function() {

  });
});

});
