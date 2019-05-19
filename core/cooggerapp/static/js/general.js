$(document).ready(function() {
  $(".report").click(function(event){
    var content_id = this.getAttribute("data-content-id");
    $("body").load(`{% url 'report' %}?content_id=${content_id}`);
  });
  $(".b-edit-point").click(function() {
      let id = this.getAttribute("data-edit-id");
      $(`.data-edit-id-${id}`).toggle();
  });
  let off_target = [
    {target:".open_footer", hide:"footer"},
    {target:".open_header_menu", hide:".header_menu"},
    {target:".close-ms", hide:".main-messages"},
    {target:".lg", hide:".languages"},
    {target:".ctg", hide:".categories"},
    {target:".lists", hide:"nav"},
    {target:".run-filter", hide:".filter-machine"},
  ];
  for (i in off_target) {
    let target = off_target[i].target;
    let hide = off_target[i].hide;
    $("*").click(function(e){
      if ( !$(e.target).is(target) && !$(e.target).is(`${target} *`) && !$(e.target).is(hide) && !$(e.target).is(`${hide} *`) ){
        $(hide).hide();
      }
    });
  }
  $(".open_footer").click(function() {
      $("footer").toggle();
  })
  $(".closed_footer").click(function() {
      $("footer").hide();
  })
  $(".open_header_menu").click(function() {
      $(".header_menu").toggle();
  })
  $(".close-ms").click(function() {
      $(".main-messages").remove();
  })
  $(".lg").click(function() {
      $(".languages").toggle();
  });
  $(".ctg").click(function() {
      $(".categories").toggle();
  });
  $(".utopic-open").click(function() {
      $(".utopic").toggle();
  });
  $(".run-filter").click(function() {
      $(".filter-machine").toggle();
  });
  // ad deceted
  let adBlockEnabled = false;
  let ads = document.createElement('div');
  ads.innerHTML = '&amp;nbsp;';
  ads.className = 'adsbox';
  document.body.appendChild(ads);
  if (window.location.pathname != "/adblock/"){
    window.setTimeout(function() {
      if (ads.offsetHeight === 0) {adBlockEnabled = true;}
      ads.remove();
      if (adBlockEnabled) {window.location = "/adblock";}
      }, 100
    );
  }
  else{
    window.setTimeout(function() {
      if (ads.offsetHeight === 0) {adBlockEnabled = true;}
      ads.remove();
      if (!adBlockEnabled) {window.location = "/";}
      }, 100
    );
  }
  // ad deceted
});