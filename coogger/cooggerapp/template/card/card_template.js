let card = "";
{% if introduction %}
  card = `<card data-postid="${content_id}" id="${author}-${permlink}" general="br-2 bg-white w-30" mobile-s="w-100"
  mobile-m="w-98" mobile-l="w-98" tablet="w-80" laptop="w-40" laptop-l="w-30"
  max="w-30" style="margin:6px;">`;
{% else %}
  card = `<card data-postid="${content_id}" id="${author}-${permlink}" general="br-2 bg-white">`;
{% endif %}
let card_output = `${card}
{% if request.user.is_authenticated %}
  <div general="br-1 bg-secondary" animation-hover="bg-danger" class="b-edit-point" data-edit-id=${content_id}>
    <div class="bebordert"></div>
    <div class="beborder"></div>
    <div class="beborderb"></div>
  </div>
<div flex="jc-c ai-c" general="bg-success" class="b-edit-panel data-edit-id-${content_id}" style="display: none;">
  {% if ct.user == request.user %}
  <a flex="ai-c" hover="c-white" general="c-white" href="/post/change/@${author}/${permlink}" flex="ai-c" style="height: 100%;">
    <i class="fa fa-edit fa" aria-hidden="true" style="margin-left: 12px;"></i>
    <div general="txt-s" style="margin-left:6px;">Edit</div>
  </a>
  {% endif %}
  {% if ct.user != request.user %}
  <div flex="ai-c" class="report" data-content-id=${content_id} general="bg-danger" style="height: 100%;cursor:pointer;">
    <i general="c-white" class="fa fa-flag fa" aria-hidden="true" style="margin-left: 12px;"></i>
    <div general="txt-s c-white" style="margin-left:6px;">Report</div>
  </div>
{% endif %}
</div>
{% endif %}
<div general="b-1 br-2 brc-white" style="padding: 6px 12px;">
  <div flex="ai-c">
    <a general="txt-m c-dark" href="/@${author}" id="author_href" flex="ai-c" animation-hover="c-private">
      <img class="carduserimg" general="br-circle" width="40px" height="40px" src=https://steemitimages.com/u/${author}/avatar>
        <div flex="fd-c">
          <span flex="ai-c" class="carduser" style="margin-left:6px;">@${author} -
            <span general="txt-s br-2 c-seconday" style="padding: 2px" id="reputation">${rep}</span>
            <span general="txt-s c-secondary"> | ${dapp_name}</span>
          </span>
          <span general="txt-xs c-dark" style="margin-left:6px;" id="created">
            <i class="fas fa-clock"></i>
              <span class="capitalize" id="created">${created}</span>
          </span>
        </div>
    </a>
  </div>
</div>
<div flex="jc-fs" general="txt-l" style="margin: 12px 12px;">
  <a class="capitalize" href=/@${author}/${permlink} id="absolute_url_href">
    <strong id="title" general="c-dark">${title}</strong>
  </a>
</div>
<div general="br-2 c-secondary c-dark" flex="ai-fs" style="margin: 12px 0px;">
  <div general="txt-s" flex="ai-c" class="duread-li">
    <div class="capitalize" style="margin-left: 12px;" flex="ai-fe">
      <i class="fab fa-readme" style="margin: 0px 6px 0px 0px;"></i>
      ${duration_of_read}
    </div>
  </div>
  <div general="txt-s" flex="ai-c" class="duread-li">
      <div class="capitalize" style="margin-left: 12px;">
        <i class="fas fa-eye"></i>
        views ${views}
      </div>
  </div>
  <div general="txt-s" flex="ai-c" class="duread-li">
      <div class="capitalize" style="margin-left: 12px;">
        <i class="fas fa-reply"></i>
        reply ${reply}
      </div>
  </div>
  <div general="txt-s" flex="ai-c" class="duread-li">
      <div class="capitalize" style="margin-left: 12px;">
        <i class="fas fa-chevron-circle-up"></i>
        votes ${votes}
      </div>
  </div>
</div>
<div flex style="margin: 12px 12px;">

<div flex="ai-c" general="txt-s left c-white" class="content_list">
    <a class="capitalize" hover="c-white bg-primary" general="b-1 br-2 c-primary" id="topic"
      href="/topic/${topic}/" style="padding: 2px 6px;">
      <i class="fa fa-hashtag" aria-hidden="true"></i>${topic}</a>
</div>
<div flex="ai-c" general="txt-s right c-white" class="content_list">
    <a class="capitalize" hover="c-white bg-primary" general="b-1 br-2 c-primary"
     href="/category/${category}" id="category" style="padding: 2px 6px;">
     <i class="fa fa-list-alt" aria-hidden="true"></i>${category}</a>
</div>
</div>
<a href=/@${author}/${permlink} id="absolute_url_href" general="c-dark">
  <div general="txt-m" class="upshow">
    <div flex="ai-c">
      ${definition}
    </div>
  </div>
</a>
<div flex="jc-fe" style="padding: 6px 12px;" general="br-2 c-secondary">
  <div general="txt-s" flex="ai-c" class="duread-li" style="margin-right: auto;">
    <div class="ctpayout" general="b-1 br-2 c-white bg-success" style="margin:0px 2px;padding: 2px 6px;">
      $<span id="post_reward_total">${post_reward_total}</span>
    </div>
  </div>
  <div flex="ai-c" general="txt-s right c-white" class="content_list">
  <a class="capitalize" hover="c-white bg-primary" general="b-1 br-2 c-primary" href="/language/${language}" id="language" style="margin:0px 2px;padding: 2px 6px;">
    <i class="fas fa-flag"></i>
    ${language}</a>
  </div>
</div>
</card>`;
