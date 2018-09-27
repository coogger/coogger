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

function timeSince(date){
  var seconds = Math.floor((new Date() - new Date(date)) / 1000);
  var year = Math.floor(seconds / 31536000);
  if (year>1){
    seconds = Math.floor(seconds - (year*31536000));
    year = year+" year";
  }
  else{
    year = "";
  }
  var months = Math.floor(seconds / 2592000);
  if (months>1){
    seconds = Math.floor(seconds - (months*2592000));
    months = months+" month";
  }
  else{
    months = "";
  }
  var days = Math.floor(seconds / 86400);
  if (days>1){
    seconds = Math.floor(seconds - (days*86400));
    days = days+" day";
  }
  else{
    days = "";
  }
  var hours = Math.floor(seconds / 3600);
  if (hours>1){
    seconds = Math.floor(seconds - (hours*3600));
    hours = hours+" hours";
  }
  else{
    hours = "";
  }
  var minutes = Math.floor(seconds / 60);
  if (minutes>1){
    seconds = Math.floor(seconds - (minutes*60));
    minutes = minutes+" minute";
  }
  else{
    minutes = "";
  }
  if (seconds>1){
    seconds = seconds+" second";
  }
  else{
    seconds = "";
  }

  return (year+" "+months+" "+days+" "+hours+" "+minutes+" "+seconds+" | ago");
}
