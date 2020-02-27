// let csrfToken = document.getElementsByTagName("meta").datas.dataset["csrf"];
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
function getRepliesTemplate(reply) {
  if (reply.reply) {
    return (
      `<div class="comment_replies" id="reply-id-${reply.id}">
        ${replyUserInfo(reply)} ${replyBody(reply)}
      </div>`
    );
  }
  return (
    `<div class="comment" id="reply-id-${reply.id}">
      <div class="comment_highlighted">
        ${replyUserInfo(reply)} ${replyBody(reply)}
      </div>
    </div>`
  );
}
$(document).ready(function () {
  $("#send-reply").click(function () {
    let this_ = this;
    let getComment = $("#id_body").val();
    if (getComment !== "") {
      $(this_).attr("class", "make_reply_animation");
      $.ajax({
        type: "POST",
        url: $(this).data("request-url"),
        data: {
          "body": getComment,
          "content_type": $(this).data("content-type"),
          "object_id": $(this).data("object-id"),
          "reply": $(this).data("reply"),
        },
        beforeSend: function (xhr) {
          xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
      }).done(function (newReply) {
        document.getElementById("id_body").value = "";
        $("#comment_template").append(getRepliesTemplate(newReply));
      }).always(function () {
        $(this_).removeClass("make_reply_animation");
      });
    }
    else {
      alert("Empty comments cannot be published.");
    }
  })
});
function getDataFromCooggerapi(apiUrl) {
  return fetch(apiUrl)
    .then((resp) => resp.json())
    .then(function (data) {
      return data;
    })
    .catch(function (error) {
      console.log("request failed", error)
    });
}
let getResultFromCooggerApi = function (apiUrl) {
  return getDataFromCooggerapi(apiUrl).then(function (data) {
    return data.results;
  });
}
function replyUserInfo(comment) {
  let title = comment.title;
  let title_template = "";
  if (title !== "user") {
    `<span class="uppercase" general="bg:danger color:white text:xs br:2" style="margin-left: 6px; padding:2px 4px;">
      ${title.toUpperCase()}
    </span>`
  }
  return (`
    <div general="bg:white" style="border-bottom: 1px solid #eaecee;">
    <div general="flex flex:ai-fs bg:white" style="padding: 12px 0px;">
      <img general="br:circle position:left" id="detail_profile_image" src="${comment.avatar_url}" style="height:  40px;width:  40px;margin:  initial;">
      <div general="flex text:s flex:fd-c">
          ${title_template}
          <a general="flex" title="${comment.username}" href="/@${comment.username}" style="padding: 0px 6px;word-wrap: break-word;word-break: break-all;">
            <span id="username">
            ${comment.username}
            </span>
          </a>
          <div general="color:secondary">
            <i class="fas fa-clock"></i>
            <span id="time">${timeSince(comment.created)}</span>
          </div>
      </div>
          <a general="color:primary:hover" target="_blank" href="https://www.github.com/${comment.username}">
      <i general="flex flex:ai-c" class="fab fa-github"></i>
    </a>
        <div general="flex text:s position:right flex:ai-c" class="just-pc">
            <div style="margin-right: 12px;">
              <i class="fas fa-clock"></i>
              Last update | <span id="lastmod">${timeSince(comment.updated)}</span>
            </div>
          </div>
    </div>
    <div general="fd-s"></div>
  </div>`
  );
}
function replyBody(reply) {
  let title = reply.title;
  let id = reply.id;
  let upvoteCount = reply.upvote_count;
  if (upvoteCount === null) {
    upvoteCount = 0;
  }
  let views = reply.views;
  if (views === null) {
    views = 0;
  }
  let replyCount = reply.reply_count;
  if (replyCount === null) {
    replyCount = 0;
  }
  $(function () {
    let Editor = editormd.markdownToHTML(reply.id + "_arg_editormd", {
      height: 670,
      path: "/static/lib/",
      htmlDecode: "html, iframe",
      markdown: reply.body,
      atLink: false,
    });
  });
  return (`
      <div style="padding: inherit;">
        <div style="width: auto;height: auto;border: none;" class="editormd font-comfortaa" id="${id}_arg_editormd">
            <textarea style="display:none;" id="editormd_content"></textarea>
        </div>
      </div>
      <div general="flex flex:ai-c br:2 color:secondary br:2 brc:muted position:right" style="padding: 2px 4px;">
          <div general="text:s flex flex:ai-c">
            <a href="${reply.get_absolute_url}" id="root_content" target="blank" general="text:s">
              <span style="margin: 0px 6px" general="color:orange">Reply</span>
            </a>
          </div>
          <div general="text:s flex flex:ai-c">
              <i class="fas fa-heart"></i>
              <div style="margin-left: 6px;">${upvoteCount}</div>
          </div>
          <div general="text:s flex flex:ai-c">
              <i class="fas fa-eye"></i>
              <div style="margin-left: 6px;">${views}</div>
          </div>
          <div general="text:s flex flex:ai-c">
              <i class="fas fa-reply-all"></i>
              <div style="margin-left: 6px;">${replyCount}</div>
          </div>
        </div>
    `);
}

function getChildrenReplies(reply, requestUrl, depth) {
  if (reply.reply_count !== 0 && reply.reply_count !== undefined) {
    getResultFromCooggerApi(`${requestUrl}?reply=${reply.id}`).then(function (childrenReplies) {
      var ii;
      for (ii in childrenReplies) {
        let childrenReply = childrenReplies[ii];
        console.log((childrenReply.depth - depth));
        $(`#reply-id-${childrenReply.parent_id}`).append(getRepliesTemplate(childrenReply));
        if ((childrenReply.depth - depth) > 5) {
          $(`#reply-id-${childrenReply.parent_id}`).append(
            `<a general="color:primary position:right" href="${reply.get_absolute_url}">
                Show ${childrenReply.reply_count} more replies
              </a>`
          );
          break
        }
        getChildrenReplies(childrenReply, requestUrl, depth);
      }
    });
  }
}
function loadReplies(objectId, contentType, requestUrl) {
  let replies_api = `${requestUrl}?object_id=${objectId}&content_type=${contentType}`;
  getResultFromCooggerApi(replies_api).then(function (replies) {
    for (let i in replies) {
      let reply = replies[i];
      $("#comment_template").append(getRepliesTemplate(reply));
      getChildrenReplies(reply, requestUrl, reply.depth);
    }
  });
}
