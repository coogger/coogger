$(document).ready(function() {
  $(".report").click(function(event){
    var contentId = this.getAttribute("data-content-id");
    $("body").load(`/report/${contentId}/`);
  });
  let offTarget = [
    {target:".open_footer", hide:"footer"},
    {target:".open_header_menu", hide:".header_menu"},
    {target:".close-ms", hide:".main-messages"},
    {target:".lg", hide:".languages"},
    {target:".ctg", hide:".categories"},
    {target:".lists", hide:"nav"},
    {target:".run-filter", hide:".filter-machine"},
  ];
  var i;
  for (i in offTarget) {
    let target = offTarget[i].target;
    let hide = offTarget[i].hide;
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
});