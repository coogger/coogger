// coogger.js
  function getTagsAsTemplate(tags){
    let template = "";
    for (let index in tags) {
      template += `<div class="tag">
        <a href="/tags/${tags[index]}" general="color:white bg:dark-purple:hover" >#${tags[index]}</a>
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

$(document).ready(function() {
  // follow/unfollow operations
  $(".follow-op").click(function(event){
    $(".follow-op").addClass("make_reply_animation");
    let url = this.getAttribute("data-url");
    let followerCount = parseInt($("#follower_count").html());
    $.get(url, function(data, status){
      if (data.status === "follow"){
        if ( !isNaN(followerCount) ){
          $("#follower_count").html(followerCount + 1);
        }
        $("#follow-op #follow").html("Unfollow");
        $("#follow-op").attr({"hover":"bg:red"});
      }
      else if (data.status === "unfollow"){
        if ( !isNaN(followerCount) ){
          $("#follower_count").html(followerCount - 1);
        }
        $("#follow-op #follow").html("Follow");
        $("#follow-op").attr({"hover":"bg:primary"});
      }
    }).always(function(r){
      $(".follow-op").removeClass("make_reply_animation");
    });
  });
  let votes = document.querySelectorAll("#vote-section");
    votes.forEach(function(vote) {
      // vote
      let status = $(vote).data("vote-status");
      if (status == "False"){
        $(vote).find("#downvote").attr("general","color:danger");
      }
      else if (status == "True"){
        $(vote).find("#upvote").attr("general", "color:success");
      }
    });
    // bookmark
    let bookmarks = document.querySelectorAll(".bookmarkop");
      bookmarks.forEach(function(bookmark) {
      let bookmark_status = $(bookmark).data("bookmark-status");
      if (bookmark_status == "False"){
        $(bookmark).find(".bookmarkicon").attr("general","color:secondary");
        $(bookmark).find(".bookmarkicon").addClass("far");
      }
      else if (bookmark_status == "True"){
        $(bookmark).find(".bookmarkicon").attr("general", "color:success");
        $(bookmark).find(".bookmarkicon").addClass("fas");
      }
    });
    
});
function vote(this_){
  let status, upvote, downvote;
  if (this_.id.includes("upvote")){
      status = true;
      upvote = this_;
      downvote = this_.parentElement.lastElementChild;
  }
  else if (this_.id.includes("downvote")){
      status = false;
      upvote = this_.parentElement.firstElementChild;
      downvote = this_;
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
          if (r.status === true){
              $(upvote).attr("general", "color:success");
              $(downvote).attr("general","color:secondary color:danger:hover");
            }
          else if (r.status === false){
              $(upvote).attr("general","color:secondary color:success:hover");
              $(downvote).attr("general","color:danger");
          }
          $(upvote).text(r.upvote_count);
          $(downvote).text(r.downvote_count);
      } 
  });
}
function removeOrAddBookmark(this_){
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
          let howMany = parseInt(this_.lastElementChild.innerText);
          let bookmarkicon = $(this_).find($(".bookmarkicon"));
          if (r.status === true){
            bookmarkicon.attr("general", "color:success");
            bookmarkicon.addClass("fas");
            bookmarkicon.removeClass("far");
            $(this_.lastElementChild).html(howMany + 1);
          }
          else if (r.status === false){
            bookmarkicon.attr("general","color:secondary");
            bookmarkicon.addClass("far");
            bookmarkicon.removeClass("fas");
            $(this_.lastElementChild).html(howMany - 1);
          }
      } 
  });
}