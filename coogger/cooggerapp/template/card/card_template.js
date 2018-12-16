`<card data-postid=${content_id} id=${author}-${permlink} general="br-2 bg-white">
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
          <span general="txt-xs c-dark" style="margin-left:6px;" id="created">${created}</span>
        </div>
    </a>
  </div>
</div>
<div flex="" style="margin: 12px 12px;">
  <div flex="ai-c" general="txt-s left c-white" class="content_list">
    <a hover="c-white bg-primary" general="b-1 br-2 c-primary" id="topic" href="/${topic}/@${author}" style="padding: 2px 6px;">${topic}</a>
  </div>
  <div flex="ai-c" general="txt-s right c-white" class="content_list">
    <a hover="c-white bg-primary" general="b-1 br-2 c-primary" href="/category/${category}/" id="category" style="padding: 2px 6px;">${category}</a>
  </div>
</div>
<div general="br-2 c-secondary c-dark" flex="ai-fs" style="margin: 12px 0px;">
  <div general="txt-s" flex="ai-c" class="duread-li">
    <div style="margin-left: 12px;" id="dor">min ${duration_of_read}</div>
  </div>
  <div general="txt-s" flex="ai-c" class="duread-li">
    <div style="margin-left: 12px;">views ${views}</div>
  </div>
  <div general="txt-s" flex="ai-c" class="duread-li">
    <div style="margin-left: 12px;">reply <span id="reply">${reply}</span></div>
  </div>
  <div general="txt-s" flex="ai-c" class="duread-li">
    <div style="margin-left: 12px;">votes <span id="votes">${votes}</span></div>
  </div>
</div>
<div flex="jc-fs" general="txt-l" style="margin: 12px 12px;">
  <a href=/@${author}/${permlink} id="absolute_url_href">
    <strong id="title" general="c-dark">${title}</strong>
  </a>
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
      <a hover="c-white bg-primary" general="b-1 br-2 c-primary"
       href="/language/${language}" id="language" style="margin:0px 2px;padding: 2px 6px;">${language}</a>
  </div>
</div>
</card>`
