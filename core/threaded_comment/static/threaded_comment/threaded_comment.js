$(document).ready(function() {
  $("#send-reply").click(function(){
    this_ = this;
    let csrf_token = $(this).data("csrf");
    let request_url = $(this).data("request-url");
    let content_type = $(this).data("content-type");
    let object_id = $(this).data("object-id");
    let reply = $(this).data("reply");
    let get_comment = $("#id_body").val();
    if (get_comment != ""){
      $(this_).attr("class", "make_reply_animation");
      $.ajax({
        type: "POST",
        url: request_url,
        headers: {
          "X-CSRFToken": csrf_token
        },
        data: {
          "body": get_comment,
          "content_type": content_type,
          "object_id": object_id,
          "reply": reply,
        },
      }).done(function(new_reply) {
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
    if (reply.reply){
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
  function getChildrenReplies(reply, request_url){
    if (reply.reply_count != 0 && reply.reply_count != undefined){
      getResultFromCooggerApi(`${request_url}?reply=${reply.id}`).then(function(childrenReplies){
        var ii;
        for (ii in childrenReplies) {
          let childrenReply = childrenReplies[ii];
          let childrenCommentTemplate = getRepliesTemplate(childrenReply);
          $(`#reply-id-${childrenReply.parent_id}`).append(childrenCommentTemplate);
          getChildrenReplies(childrenReply, request_url);
        }
      });
    }
  }
  function loadReplies(object_id, content_type, request_url){
    let replies_api = `${request_url}?object_id=${object_id}&content_type=${content_type}`;
    getResultFromCooggerApi(replies_api).then(function(replies){
      for (i in replies){
        let reply = replies[i];
        $("#comment_template").append(getRepliesTemplate(reply));
        getChildrenReplies(reply, request_url);
      }
    });
  }
