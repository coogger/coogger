// coogger.js
function get_data_from_cooggerapi(apiUrl){
    return fetch(apiUrl)
      .then((resp) => resp.json())
      .then(function(data) {
        return data;
      })
      .catch(function(error) {
        console.log('request failed', error)
      });
  }
  let get_result_from_cooggerapi = function(apiUrl){
    return get_data_from_cooggerapi(apiUrl).then(function(data){
      return data.results;
    })
  }
  // coogger.js
  function content_replies(comments){
    let comment_index;
    for (comment_index = 0; comment_index < comments.length; comment_index++) {
      let comment = comments[comment_index];
      if (comment.children != 0){
        steem.api.getContentReplies(parent=comment.author, parentPermlink=comment.permlink, function (err, children_comments) {
          let children_comment_index;
          let children_comments_len = children_comments.length;
          for (children_comment_index = 0; children_comment_index < children_comments_len; children_comment_index++) {
            let children_comment_template = "";
            let children_comment = children_comments[children_comment_index];
            if (children_comment.depth<9){
              children_comment_template += `
                <div class='comment_replies'
                  id='${children_comment.author}-${children_comment.permlink}'>
                `
              children_comment_template += comment_info(children_comment);
              children_comment_template += userinfo(children_comment);
              children_comment_template += comment_body(children_comment);
              if (children_comment.depth == 8){
                children_comment_template += (`
                  <a general="center c-success"
                    href="/@${children_comment.author}/'${children_comment.permlink}">
                    Show ${children_comment.children} more content_replies
                  </a></div>`);
              }
              else{
                children_comment_template += "</div>";
              }
              $(`#${children_comment.parent_author}-${children_comment.parent_permlink}`).append(children_comment_template);
            }
          }
          content_replies(children_comments);
        });
      }
    }
  }
  function getTagsAsTemplate(tags){
    let template = "";
    for (const index in tags) {
      let tag = tags[index];
      template += `<div class="tag">
        <a href="/tags/${tag}" general="c-white" hover="bg-dark-purple">#${tag}</a>
      </div>`
    }
    return template;
  }
  function copyTextFromId(id) {
    let text = document.getElementById("embed-text");
    text.select();
    document.execCommand("copy");
  }
  function get_scroll_bottom_location(){
    return $(window).scrollTop() + $(window).height()+100;
  }
  function scrolledbottom(){
    if ( get_scroll_bottom_location() >= $(document).height()){
      return true;
    }
    return false;
  }
  function dor(text){
    // post duration of read
    let reading_speed = 28;
    return `min ${((text.length/reading_speed)/60).toFixed(1)}`;
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
  // issue reply
  function reply_info(get_absolute_url){
    return (`
    <div flex style='margin: 12px 0px' general='c-white br-2' class='root_content'>
      <div>
        <li flex='ai-c'>
          <a href='${get_absolute_url}' id='root_content' target='blank' general='txt-s'>
          <span style='margin: 0px 6px' general='c-secondary'>Open in new tab to view more detailed</span>
          </a>
        </li>
      </div>
    </div>`);
  }
  function reply_userinfo(comment){
    return (`
      <div style='border-bottom: 1px solid #eaecee;margin: 4px 0px;padding: 8px 0px;'>
        <div flex='ai-fs' general='bg-white'>
        <a flex title='${comment.username}' href='/@${comment.username}'
          style='padding: 0px 6px;word-wrap: break-word;word-break: break-all;'>
            <img general='br-circle left' id='detail_profile_image' src='${comment.avatar_url}' class='useruserimg' style='height:  40px;width:  40px;margin:  initial;'>
          </a>
          <div general='txt-s' flex='fd-c' class='duread-li'>
              <a flex title='${comment.username}' href='/@${comment.username}'
                style='padding: 0px 6px;word-wrap: break-word;word-break: break-all;'>
              @${comment.username}<span id='username'></span>
          </a>
              <div style='margin-left: 8px;' general='c-secondary'>${timeSince(comment.created)}</div>
          </div>
          <a hover="c-primary" target="_blank" href="https://www.github.com/${comment.username}">
            <i flex="ai-c" class="fab fa-github"></i>
          </a>
        </div>
      </div>`
    );
  }
  function reply_body(reply){
    let title = reply.title;
    let id = reply.id;
    let upvote_count = reply.upvote_count;
    if (upvote_count == null){
      upvote_count = 0;
    }
    let views = reply.views;
    if (views == null){
      views = 0;
    }
    let reply_count = reply.reply_count;
    if (reply_count == null){
      reply_count = 0;
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
      <div general='br-2 c-secondary br-2 brc-muted right' style='padding: 2px 4px;' flex='ai-c'>
          <div general='txt-s' flex='ai-c' class='duread-li'>
              <i class="fas fa-heart"></i>
              <div style='margin-left: 6px;'>${upvote_count}</div>
          </div>
          <div general='txt-s' flex='ai-c' class='duread-li'>
              <i class="fas fa-eye"></i>
              <div style='margin-left: 6px;'>${views}</div>
          </div>
          <div general='txt-s' flex='ai-c' class='duread-li'>
              <i class="fas fa-reply-all"></i>
              <div style='margin-left: 6px;'>${reply_count}</div>
          </div>
        </div>
    `);
  }
  function get_children_replies(reply, api_name){
    if (reply.reply_count != 0 && reply.reply_count != undefined){
      get_result_from_cooggerapi(`/api/${api_name}/?reply=${reply.id}`).then(function(children_replies){
        for (ii in children_replies) {
          let children_reply = children_replies[ii];
          let children_comment_template = get_replies_template(children_reply);
          $(`#${children_reply.parent_username}-${children_reply.parent_permlink}`).append(children_comment_template);
          get_children_replies(children_reply, api_name);
        }
      });
    }
  }
  function load_replies(id, api_name){
    let replies_api = `/api/${api_name}/?reply=${id}`;
    get_result_from_cooggerapi(replies_api).then(function(replies){
      for (i in replies){
        let reply = replies[i];
        $("#comment_template").append(get_replies_template(reply));
        get_children_replies(reply, api_name);
      }
    });
  }
function get_replies_template(reply){
  if (reply.parent_permlink.includes("re-")){
    return (
      `<div class='comment_replies' id='${reply.username}-${reply.permlink}'>
      ${reply_info(reply.get_absolute_url)} ${reply_userinfo(reply)} ${reply_body(reply)}</div>`
     );
  }
  return (
    `<div class='comment' id='${reply.username}-${reply.permlink}' <div class='comment_highlighted'>
    ${reply_info(reply.get_absolute_url)} ${reply_userinfo(reply)} ${reply_body(reply)}</div></div>`
   );
}

$(document).ready(function() {
  $("#send-reply").click(function(){
    $(this).attr("animation-hover", "i blink");
    let csrf_token = $(this).data("csrf");
    let get_comment = $("#id_body").val();
    if (get_comment != ""){
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
        $(this).attr("animation-hover", "null");
        let new_reply_template = get_replies_template(new_reply);
        $("#comment_template").append(new_reply_template);
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
              $(`#vote-section #upvote`).attr("general", "c-success");
              $(`#vote-section #downvote`).attr("general", "c-secondary");
          }
          else if (r.status == false){
              $(`#vote-section #upvote`).attr("general", "c-secondary");
              $(`#vote-section #downvote`).attr("general", "c-danger");
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
              $(this_).find($(".fa-bookmark")).attr("general", "c-success");
              $(this_).find($("#how_many_mark")).html(how_many + 1);
          }
          else if (r.status == false){
            $(this_).find($(".fa-bookmark")).attr("general", "c-secondary");
            $(this_).find($("#how_many_mark")).html(how_many - 1);
          }
      } 
  });
}