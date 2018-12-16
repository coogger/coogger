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
        $(`.data-edit-id-${data_edit_id}`).toggle("fast");
    });
    $(".lists").click(function() {
        $("nav").toggle("fast");
    });
});
// function update_account(metadata){
//     api.updateUserMetadata(metadata, function (err, res) {
//       console.log(err, res)
//     });
// }
function copyTextFromId(id) {
  let text = document.getElementById("embed-text");
  text.select();
  document.execCommand("copy");
}
// convert images url to steemitimages in cards
function update_images(query){
  let images = document.querySelectorAll(query);
  images.forEach(changeImages);
  function changeImages(images){
    if (!images.src.startsWith("https://steemitimages.com/0x0/")){
        images.src = `https://steemitimages.com/0x0/${images.src}`;
      }
  }
}
// convert images url to steemitimages in cards
function get_scroll_bottom_location(){
  return $(window).scrollTop() + $(window).height()+500;
}
function scrolledbottom(){
  if ( get_scroll_bottom_location() >= $(document).height()){
    return true;
  }
  return false;
}
function dor(text){
  // post duration of read
  let reading_speed = 20;
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
function comment_info(comment){
  return (`
  <div flex style='margin: 12px 0px' general='c-white br-2' class='root_content'>
    <div>
      <li flex='ai-c'>
        <a href='/@${comment.author}/${comment.permlink}' id='root_content' target='blank' general='txt-s'>
        <span style='margin: 0px 6px' general='c-secondary'>Open in new tab to view more detailed</span>
        </a>
      </li>
    </div>
  </div>`);
}
function userinfo(comment){
  let reputation = steem.formatter.reputation(comment.author_reputation);
  return (`
    <div style='border-bottom: 1px solid #eaecee;margin: 4px 0px;padding: 8px 0px;'>
      <div flex='ai-fs' general='bg-white'>
        <img general='br-circle left' id='detail_profile_image' src='https://steemitimages.com/u/${comment.author}/avatar' class='useruserimg'
          style='height:  40px;width:  40px;margin:  initial;'></a>
        <div general='txt-s' flex='fd-c' class='duread-li'>
            <a flex title='${comment.author}' href='/@${comment.author}'
              style='padding: 0px 6px;word-wrap: break-word;word-break: break-all;'>
            @${comment.author}<span id='username'></span> - (${reputation})
        </a>
            <div style='margin-left: 8px;' general='c-secondary'>${timeSince(comment.created)}</div>
        </div>
      </div>
    </div>`
  );
}
function comment_body(comment){
  let pending_payout_value = parseFloat(comment.pending_payout_value.replace(" SBD", ""));
  let post_reward_total = 0;
  if (pending_payout_value == 0){
    let total_payout_value = parseFloat(comment.total_payout_value.replace(" SBD", ""))
    let curator_payout_value = parseFloat(comment.curator_payout_value.replace(" SBD", ""));
    post_reward_total = total_payout_value+curator_payout_value;
  }
  else{
    post_reward_total = pending_payout_value;
  }
  post_reward_total = post_reward_total.toFixed(2);
  let title = comment.title;
  $(function() {
    editormd.urls.atLinkBase ="https://www.coogger.com/@"
    let Editor = editormd.markdownToHTML(comment.id+"_arg_editormd", {
      height: 670,
      path : '/static/lib/',
      htmlDecode: 'html, iframe',
      markdown : comment.body,
    });
  });
  return (`
    <h1 general='center txt-xl' id='title' style='width: 96%;margin: 12px auto;'>${title}</h1>
    <div style='padding: inherit;'>
      <div style='width: auto;height:  auto;border: none;' class='editormd' id='${comment.id}_arg_editormd'>
          <textarea style='display:none;' id='editormd_content'></textarea>
      </div>
    </div>
    <div general='br-2 c-secondary br-2 brc-muted right' style='padding: 2px 4px;' flex='ai-c'>
        <div general='txt-s' flex='ai-c' class='duread-li'>
            <div style='margin-left: 12px;'>reply ; ${comment.children}</div>
        </div>
        <div general='txt-s' flex='ai-c' class='duread-li'>
           <div style='margin-left: 12px;'>votes ; ${comment.net_votes}</div>
        </div>
        <div general='txt-s' flex='ai-c' class='duread-li'>
           <div style='margin-left: 12px;' general='c-success'> $ ${post_reward_total}</div>
        </div>
      </div>
  `);
}
