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

function timeSince(date) {

  var seconds = Math.floor((new Date() - date) / 1000);

  var interval = Math.floor(seconds / 31536000);

  if (interval > 1) {
    return interval + " years";
  }
  interval = Math.floor(seconds / 2592000);
  if (interval > 1) {
    return interval + " months";
  }
  interval = Math.floor(seconds / 86400);
  if (interval > 1) {
    return interval + " days";
  }
  interval = Math.floor(seconds / 3600);
  if (interval > 1) {
    return interval + " hours";
  }
  interval = Math.floor(seconds / 60);
  if (interval > 1) {
    return interval + " minutes";
  }
  return Math.floor(seconds) + " seconds";
}

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

function comment_info(comment){
  var last_update = timeSince(comment.last_update);
  var pending_payout_value = parseFloat(comment.pending_payout_value.replace(" SBD", ""));
  var post_reward_total = 0;
  if (pending_payout_value == 0){
    var total_payout_value = parseFloat(comment.total_payout_value.replace(" SBD", ""))
    var curator_payout_value = parseFloat(comment.curator_payout_value.replace(" SBD", ""));
    post_reward_total = total_payout_value+curator_payout_value;
  }
  else{
    post_reward_total = pending_payout_value;
  }
  post_reward_total = post_reward_total.toFixed(2);
  return ("\
  <div gnrl='br-2 c-secondary br-2 b-1 brc-muted right' style='padding: 2px 4px;' flx='ai-c'>\
      <div gnrl='txt-s' flx='ai-c' class='duread-li'>\
          <div style='margin-left: 12px;'>"+last_update+"</div>\
      </div>\
      <div gnrl='txt-s' flx='ai-c' class='duread-li'>\
          <div style='margin-left: 12px;'> | reply ; "+comment.children+"</div>\
      </div>\
      <div gnrl='txt-s' flx='ai-c' class='duread-li'>\
        <div style='margin-left: 12px;'> | votes ; "+comment.active_votes.length+"</div>\
      </div>\
      <div gnrl='txt-s' flx='ai-c' class='duread-li'>\
        <div style='margin-left: 12px;'> | $"+post_reward_total+"</div>\
      </div></div>\
  <div flx style='margin: 12px 0px' gnrl='bg-muted c-white br-2' class='root_content'>\
    <div style='width: 100%;'>\
      <li flx='ai-c'>\
        <a href='/@"+comment.author+"/"+comment.permlink+"' id='root_content'\
        target='blank' gnrl='c-secondary txt-s' style='color: black;padding: 8px 0px;width: 100%;'>\
        <span style='margin: 0px 6px'>Open in new tab to view more detailed</span>\
        </a>\
      </li>\
    </div>\
  </div>");
}

function userinfo(comment){
  var reputation = steem.formatter.reputation(comment.author_reputation);
  return ("\
    <div style='border-bottom: 1px solid #eaecee;margin: 4px 0px;padding: 8px 0px;'>\
      <div flx='ai-fs' gnrl='bg-white'>\
        <img gnrl='br-circle left' id='detail_profile_image' src='https://steemitimages.com/u/"+comment.author+"/avatar' class='useruserimg'\
          style='height:  40px;width:  40px;margin:  initial;'></a>\
        <div gnrl='txt-s' flx='fd-c' class='duread-li'>\
            <a flx title='"+comment.author+"' href='/@"+comment.author+"' style='padding: 0px 6px;word-wrap: break-word;word-break: break-all;'>\
        @"+comment.author+"<span id='username'></span> - ("+reputation+")\
        </a>\
            <div style='margin-left: 8px;' gnrl='c-secondary'>"+timeSince(comment.created)+"</div>\
        </div>\
      </div>\
    </div>"
  );
}

function comment_body(comment){
  return ("\
    <h1 gnrl='center txt-xl' id='title' style='width: 96%;margin: 12px auto;'></h1>\
    <div style='padding: inherit;'>\
      <div style='width: auto;height:  auto;border: none;' class='editormd' id='"+comment.id+"_arg_editormd'>\
          <textarea style='display:none;' id='editormd_content'></textarea>\
      </div>\
    </div>\
  ");
}

function comment_body_md(comment){
  $(function() {
    var Editor = editormd.markdownToHTML(comment.id+"_arg_editormd", {
      height: 670,
      path : '/static/lib/',
      htmlDecode: 'tml,iframe',
      atLink: false,
      emailLink : false,
      markdown : comment.body,
    });
  });
}
