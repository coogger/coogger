// coogger.js
  function getTagsAsTemplate(tags){
    let template = "";
    for (const index in tags) {
      let tag = tags[index];
      template += `<div class="tag">
        <a href="/tags/${tag}" general="color:white bg:dark-purple:hover" >#${tag}</a>
      </div>`
    }
    return template;
  }
  function copyTextFromId(id) {
    let text = document.getElementById("embed-text");
    text.select();
    document.execCommand("copy");
    alert("Copied");
  }
  function dor(text){
    // post duration of read
    let readingSpeed = 28;
    return `min ${((text.length/readingSpeed)/60).toFixed(1)}`;
  }
function timeSince(date) {
  let seconds = Math.floor((new Date() - new Date(date)) / 1000);
  let interval = Math.floor(seconds / 31536000);
  let timesince = [];
  if (interval > 1) {
    seconds = (seconds - (31536000 * interval));
    timesince.push(interval + " years ");
  }
  interval = Math.floor(seconds / 2592000);
  if (interval > 1) {
    seconds = (seconds - (2592000 * interval));
    timesince.push(interval + " months ");
  }
  interval = Math.floor(seconds / 86400);
  if (interval > 1) {
    seconds = (seconds - (86400 * interval));
    timesince.push(interval + " days ");
  }
  interval = Math.floor(seconds / 3600);
  if (interval > 1) {
    seconds = (seconds - (3600 * interval));
    timesince.push(interval + " hours ");
  }
  interval = Math.floor(seconds / 60);
  if (interval > 1) {
    seconds = (seconds - (60 * interval));
    timesince.push(interval + " minutes ");
  }
  timesince.push(seconds + " seconds ");
  return timesince.slice(0, 2) + " ago";
}
$(document).ready(function() {
  // follow/unfollow operations
  $(".follow-op").click(function(event){
    $(".follow-op").addClass("make_reply_animation");
    let url = this.getAttribute("data-url");
    let follower_count = parseInt($("#follower_count").html());
    $.get(url, function(data, status){
      if (data.status == "follow"){
        if ( !isNaN(follower_count) ){
          $("#follower_count").html(follower_count + 1);
        }
        $("#follow-op #follow").html("Unfollow");
        $("#follow-op").attr({"hover":"bg:red"});
      }
      else if (data.status == "unfollow"){
        if ( !isNaN(follower_count) ){
          $("#follower_count").html(follower_count - 1);
        }
        $("#follow-op #follow").html("Follow");
        $("#follow-op").attr({"hover":"bg:primary"});
      }
    }).always(function(r){
      $(".follow-op").removeClass("make_reply_animation");
    });
  });
});

function vote(this_, id, model_name){
  let status;
  if (this_.id == "upvote"){
      status = true;
  }
  else if (this_.id == "downvote"){
      status = false;
  }
  $.ajax({
      type: "POST",
      url: $(this_).data("url"),
      data: {
          "status": status,
          "csrfmiddlewaretoken": $(this_).data("csrf"),
      },
  }).done(function(r) {
      r = JSON.parse(r);
      if (r.error){
          alert(r.error);
      }
      else{
          if (r.status == true){
              $(`#vote-section #upvote`).attr("general", "color:success");
              $(`#vote-section #downvote`).attr("general","color:secondary color:danger:hover");
          }
          else if (r.status == false){
              $(`#vote-section #upvote`).attr("general","color:secondary color:success:hover");
              $(`#vote-section #downvote`).attr("general","color:danger");
          }
          $(`#vote-section #upvote`).text(r.upvote_count);
          $(`#vote-section #downvote`).text(r.downvote_count);
      } 
  });
}
function remove_or_add_bookmark(this_){
  $.ajax({
      type: "POST",
      url: $(this_).data("url"),
      data: {
          "app_label": $(this_).data("app_label"),
          "model": $(this_).data("model"),
          "object_id": $(this_).data("object_id"),
          "csrfmiddlewaretoken": $(this_).data("csrf"),
      },
  }).done(function(r) {
      if (r.error){
          alert(r.error);
      }
      else{
          let how_many = parseInt($(this_).find($("#how_many_mark")).text());
          if (r.status == true){
              $(this_).find($(".fa-bookmark")).attr("general", "color:success");
              $(this_).find($("#how_many_mark")).html(how_many + 1);
          }
          else if (r.status == false){
            $(this_).find($(".fa-bookmark")).attr("general","color:secondary");
            $(this_).find($("#how_many_mark")).html(how_many - 1);
          }
      } 
  });
}