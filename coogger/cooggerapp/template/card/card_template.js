`<card data-postid=${content_id} id=${author}-${permlink} gnrl="br-2" color="bg-white">
{% if request.user.is_authenticated %}
  <div gnrl="br-1" color="bg-secondary" hvr-a="bg-danger" class="b-edit-point" data-edit-id=${content_id}>
    <div class="bebordert"></div>
    <div class="beborder"></div>
    <div class="beborderb"></div>
  </div>
<div flx="jc-c ai-c" color="bg-success" class="b-edit-panel data-edit-id-${content_id}" style="display: none;">
  {% if ct.user == request.user %}
  <a flx="ai-c" hvr="c-white" color="c-white" href="/post/change/@${author}/${permlink}" flx="ai-c" style="height: 100%;">
    <i class="fa fa-edit fa" aria-hidden="true" style="margin-left: 12px;"></i>
    <div gnrl="txt-s" style="margin-left:6px;">Edit</div>
  </a>
  {% endif %}
  {% if ct.user != request.user %}
  <div flx="ai-c" class="report" data-content-id=${content_id} color="bg-danger" style="height: 100%;cursor:pointer;">
    <i color="c-white" class="fa fa-flag fa" aria-hidden="true" style="margin-left: 12px;"></i>
    <div gnrl="txt-s" color="c-white" style="margin-left:6px;">Report</div>
  </div>
{% endif %}
</div>
{% endif %}
<div gnrl="b-1 br-2" color="brc-white" style="padding: 6px 12px;">
  <div flx="ai-c">
    <a gnrl="txt-m" color="c-dark" href="/@${author}" id="author_href" flx="ai-c" hvr-a="c-private">
      <img class="carduserimg" gnrl="br-circle" width="40px" height="40px" src=https://steemitimages.com/u/${author}/avatar>
        <div flx="fd-c">
          <span flx="ai-c" class="carduser" style="margin-left:6px;">@${author} -
            <span gnrl="txt-s br-2" color="c-seconday" style="padding: 2px" id="reputation">${rep}</span>
            <span gnrl="txt-s" color="c-secondary"> | ${dapp_name}</span>
          </span>
          <span gnrl="txt-xs" color="c-dark" style="margin-left:6px;" id="created">${created}</span>
        </div>
    </a>
  </div>
</div>
<div flx="" style="margin: 12px 12px;">
  <div flx="ai-c" gnrl="txt-s left" color="c-white" class="content_list">
    <a hvr="c-white bg-primary" gnrl="b-1 br-2" color="c-primary" id="language" href=/language/${language}/ style="padding: 2px 6px;">${language}</a>
  </div>
  <div flx="ai-c" gnrl="txt-s right" color="c-white" class="content_list">
    <a hvr="c-white bg-primary" gnrl="b-1 br-2" color="c-primary" href=/category/${category}/ id="category" style="padding: 2px 6px;">${category}</a>
  </div>
</div>
<div gnrl="br-2" color="c-secondary c-dark" flx="ai-fs" style="margin: 12px 0px;">
  <div gnrl="txt-s" flx="ai-c" class="duread-li">
    <div style="margin-left: 12px;" id="dor">min ${duration_of_read}</div>
  </div>
  <div gnrl="txt-s" flx="ai-c" class="duread-li">
    <div style="margin-left: 12px;">reply <span id="reply">${reply}</span></div>
  </div>
  <div gnrl="txt-s" flx="ai-c" class="duread-li">
    <div style="margin-left: 12px;">views ${views}</div>
  </div>
</div>
<div flx="jc-fs" gnrl="txt-l" style="margin: 12px 12px;">
  <a href=/@${author}/${permlink} id="absolute_url_href">
    <strong id="title" color="c-dark">${title}</strong>
  </a>
</div>
<a href=/@${author}/${permlink} id="absolute_url_href" color="c-dark">
  <div gnrl="txt-m" class="upshow">
    <div flx="ai-c">
      ${definition}
    </div>
  </div>
</a>
<div flx="jc-fe" style="padding: 6px 12px;" gnrl="br-2" color="c-secondary">
  <div gnrl="txt-s" flx="ai-c" class="duread-li" style="margin-right: auto;">
    <div class="ctpayout" gnrl="b-1 br-2" color="c-success" style="margin:0px 2px;padding: 2px 6px;">
      $<span id="post_reward_total">${post_reward_total}</span>
    </div>
  </div>
  <div class="upvote" id="upvote" data-id=${author}-${permlink} data-user=${author} data-permlink=${permlink} flx="" gnrl="br-2 txt-s" color="c-primary" style="padding: 4px 4px;cursor:pointer;">
    <i color="c-primary" hvr="c-danger" class="fa fa-thumbs-up"></i>
  </div>
</div>
</card>`
