$(document).ready(function() {
  function delete_content(this_){//içerik silmek için
    var conf = confirm("Silmek istediğinize eminmisiniz ! bu işlem geri alınamaz");
    if (conf) {
      var delete_id = this_.getAttribute("data-post-id");
      $(".error").load("/delete/" + delete_id);
      $(".b-messages").css({ display: "block" });
      $(".data-post-id-" + delete_id).remove();
      setTimeout(function() {
        $(".b-messages").css({ display: "none" });
      }, 3000);
    }
  }

  $(".open").mouseover(function() {
    $(".b-blogs").css("filter", "blur(3px)");
    $(".d-detail").css("filter", "blur(3px)");

  }).mouseout(function() {
    $(".b-blogs").css("filter", "blur(0px)");
    $(".d-detail").css("filter", "blur(0px)");
  });

  $(".delete").click(function() {
    delete_content(this);
  });
  /* detail delete  */
  $(".d-delete").click(function() {
    delete_content(this);
  });
  var wid = parseInt($(window).width());
  if (wid < 1160) { // mobil ve tablet
    //  $(".h-header-ul").addClass("wincenter");
    $(".open-header").click(function() {
      $(".h-header").toggle("fast")
    });
  }
  // her zaman çalışacak kodlar
  $(".close-ms").click(function() {
    $(".main-messages").remove();
  })
$(".b-content").mouseover(function() {
  $(this).find(".b-cont").css("opacity","0.1");
  $(this).find(".duread-main").css("opacity","1");
  var url = this.getAttribute("data-url");
  $(this).click(function() {
    window.location = "/" + url
  });
}).mouseout(function() {
  $(this).find(".b-cont").css("opacity","1");
  $(this).find(".duread-main").css("opacity","0");
});
$(".b-edit-point").click(function() {
  var data_edit_id = this.getAttribute("data-edit-id");
  $(".data-edit-id-" + data_edit_id).toggle("fast");
});
$(".d-starts-li").click(function() {
  var stars_id = this.getAttribute("data-starts-id");
  var post_id = this.getAttribute("data-post-id");
  $(".d-starts-ul").load("/stars/" + post_id + "/" + stars_id);
});
// controls
$("#id_category").change(function() {
  var str = "";
  $("#id_category option:selected").each(function() {
    str += $(this).val();
    $("#id_subcategory").load("/chosesub/" + str);
    $("#id_category2").load("/chosenone/");
  });
});
$("#id_subcategory").change(function() {
  var str = "";
  $("#id_subcategory option:selected").each(function() {
    str += $(this).val();
    $("#id_category2").load("/chosecat2/" + str);
  });
});
// controls
//--------------
//users
$(".u-i").mouseover(function() {
  $(".u-uploadform").css({ display: "block" });
}).mouseout(function() {
  $(".u-uploadform").css({ display: "none" });
});
  });
