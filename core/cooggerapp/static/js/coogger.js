// coogger.js
function getDataFromCooggerapi(apiUrl){
    return fetch(apiUrl)
      .then((resp) => resp.json())
      .then(function(data) {
        return data;
      })
      .catch(function(error) {
        console.log('request failed', error)
      });
  }
  let getResultFromCooggerApi = function(apiUrl){
    return getDataFromCooggerapi(apiUrl).then(function(data){
      return data.results;
    });
  }
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
  // issue reply
  function replyUserInfo(comment){
    return (`
      <div style='border-bottom: 1px solid #eaecee;margin: 4px 0px;padding: 8px 0px;'>
        <div general='flex flex:ai-fs bg:white'>
        <a general="flex" title='${comment.username}' href='/@${comment.username}'
          style='padding: 0px 6px;word-wrap: break-word;word-break: break-all;'>
            <img general='br:circle position:left' id='detail_profile_image' src='${comment.avatar_url}' style='height:  40px;width:  40px;margin:  initial;'>
          </a>
          <div general='text:s' general='flex flex:fd-c'>
              <a general="flex" title='${comment.username}' href='/@${comment.username}'
                style='padding: 0px 6px;word-wrap: break-word;word-break: break-all;'>
              @${comment.username}<span id='username'></span>
          </a>
              <div style='margin-left: 8px;' general='color:secondary'>${timeSince(comment.created)}</div>
          </div>
          <a general="color:primary:hover" target="_blank" href="https://www.github.com/${comment.username}">
            <i general="flex flex:ai-c" class="fab fa-github"></i>
          </a>
        </div>
      </div>`
    );
  }
  function reply_body(reply){
    let title = reply.title;
    let id = reply.id;
    let upvoteCount = reply.upvote_count;
    if (upvoteCount == null){
      upvoteCount = 0;
    }
    let views = reply.views;
    if (views == null){
      views = 0;
    }
    let replyCount = reply.reply_count;
    if (replyCount == null){
      replyCount = 0;
    }
    $(function() {
      let Editor = editormd.markdownToHTML(reply.id+"_arg_editormd", {
        height: 670,
        path : '/static/lib/',
        htmlDecode: 'html, iframe',
        markdown : reply.body,
        atLink: false,
      });
    });
    return (`
      <div style='padding: inherit;'>
        <div style='width: auto;height:  auto;border: none;' class='editormd' id='${id}_arg_editormd'>
            <textarea style='display:none;' id='editormd_content'></textarea>
        </div>
      </div>
      <div general='flex flex:ai-c br:2 color:secondary br:2 brc:muted position:right' style='padding: 2px 4px;'>
          <div general='text:s flex flex:ai-c'>    
            <a href='${reply.get_absolute_url}' id='root_content' target='blank' general='text:s'>
              <span style='margin: 0px 6px' general='color:orange'>Reply</span>
            </a>
          </div>
          <div general='text:s flex flex:ai-c'>
              <i class="fas fa-heart"></i>
              <div style='margin-left: 6px;'>${upvoteCount}</div>
          </div>
          <div general='text:s flex flex:ai-c'>
              <i class="fas fa-eye"></i>
              <div style='margin-left: 6px;'>${views}</div>
          </div>
          <div general='text:s flex flex:ai-c'>
              <i class="fas fa-reply-all"></i>
              <div style='margin-left: 6px;'>${replyCount}</div>
          </div>
        </div>
    `);
  }
  function getRepliesTemplate(reply){
    if (reply.parent_permlink.includes("re-")){
      return (
        `<div class='comment_replies' id='reply-id-${reply.id}'>
        ${replyUserInfo(reply)} ${reply_body(reply)}</div>`
       );
    }
    return (
      `<div class='comment' id='reply-id-${reply.id}' <div class='comment_highlighted'>
      ${replyUserInfo(reply)} ${reply_body(reply)}</div></div>`
     );
  }
  function getChildrenReplies(reply, api_name){
    if (reply.reply_count != 0 && reply.reply_count != undefined){
      getResultFromCooggerApi(`/api/${api_name}/?reply=${reply.id}`).then(function(childrenReplies){
        var ii;
        for (ii in childrenReplies) {
          let childrenReply = childrenReplies[ii];
          let childrenCommentTemplate = getRepliesTemplate(childrenReply);
          $(`#reply-id-${childrenReply.parent_id}`).append(childrenCommentTemplate);
          getChildrenReplies(childrenReply, api_name);
        }
      });
    }
  }
  function loadReplies(id, api_name){
    let replies_api = `/api/${api_name}/?reply=${id}`;
    getResultFromCooggerApi(replies_api).then(function(replies){
      for (i in replies){
        let reply = replies[i];
        $("#comment_template").append(getRepliesTemplate(reply));
        getChildrenReplies(reply, api_name);
      }
    });
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
  // make reply
  $("#send-reply").click(function(){
    this_ = this;
    let csrf_token = $(this).data("csrf");
    let get_comment = $("#id_body").val();
    if (get_comment != ""){
      $(this_).attr("class", "make_reply_animation");
      $.ajax({
        type: "POST",
        url: window.location.href,
        data: {
          "body": get_comment,
          "csrfmiddlewaretoken": csrf_token,
        },
      }).done(function(new_reply) {
        new_reply = JSON.parse(new_reply);
        document.getElementById("id_body").value = ""
        let new_reply_template = getRepliesTemplate(new_reply);
        $("#comment_template").append(new_reply_template);
      }).always(function(){
        $(this_).removeClass("make_reply_animation");
      });
    }
    else{
      alert("Empty comments cannot be published.")
    }
  })
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