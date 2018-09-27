$(document).ready(function() {
    $(".close-ms").click(function() {
        $(".main-messages").remove();
    })
    $(".open_header_menu").click(function() {
        $(".closed_header_menu").css({"display":"flex"});
        $(".header_menu").toggle("fast", function(){
          $(".header_menu").css({"display":"flex"});
        });
    })
    $(".closed_header_menu").click(function() {
        $(".closed_header_menu").css({"display":"none"});
        $(".header_menu").toggle("fast", function() {});
    })
    $(".b-edit-point").click(function() {
        var data_edit_id = this.getAttribute("data-edit-id");
        $(".data-edit-id-" + data_edit_id).toggle("fast");
    });
    $(".lists").click(function() {
        $("nav").toggle("fast");
    });
    if($(window).width() < 800)
    {
        $("header").attr("gnrl", "br-1 bg-white");
    } else {
        $("header").attr("gnrl", "br-1 bg-white center");
    }
});

function format_of_time(created_time){
  var created = new Date(created_time);
  var new_data = new Date();
  var created_year = created.getFullYear() - new_data.getFullYear();
  var created_mon = created.getMonth() - new_data.getMonth();
  var created_day = created.getDay() - new_data.getDay();
  var created_hours = created.getHours() - new_data.getHours();
  var created_minute = created.getMinutes() - new_data.getMinutes();
  if (created_year>=1){
    created_year = created_year+" year";
  }
  else{
    created_year = "";
  }
  if (created_mon>=1){
    created_mon = created_mon+" month";
  }
  else{
    created_mon = "";
  }
  if (created_day<8 && created_day>0){
    created_day = created_day+" day";
  }
  else{
    created_day = "";
  }
  if (created_hours<49 && created_hours>0){
    created_hours = created_hours+" hours";
  }
  else{
    created_hours = "";
  }
  if (created_minute<60 && created_minute>0){
    created_minute = created_minute+" minute";
  }
  else{
    created_minute = "";
  }
  return (created_year+" "+created_mon+" "+created_day+" "+created_hours+" "+created_minute+" "+"ago");
}
