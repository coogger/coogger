$(document).ready(function() {
    function set() {
        var wid = $(window).width();
        var heig = $(window).height();
        if (wid < 1160) {
            var free_space = 0;
        } else {
            var free_space = 320;
            // h-nav-ul ayarlama
            $(".h-nav-ul").mouseover(function() {
                $(".h-nav-ul").css("overflow", "auto");
                $(".h-nav-ul").css("height", "auto");
                $(".b-blogs").css("filter", "blur(3px)");
            }).mouseout(function() {
                $(".h-nav-ul").css("overflow", "hidden");
                $(".h-nav-ul").css("height", 40);
                $(".b-blogs").css("filter", "blur(0px)");
            });
        }
        $(".h-notifications-ul").mouseover(function() {
            $(".h-notifications-ul").css("overflow", "auto");
            $(".h-notifications-ul").css("height", "auto");
            $(".b-blogs").css("filter", "blur(3px)");
        }).mouseout(function() {
            $(".h-notifications-ul").css("overflow", "hidden");
            $(".h-notifications-ul").css("height", 40);
            $(".b-blogs").css("filter", "blur(0px)");
        });
        var total_wid = wid - free_space; // ekranda boş kalan yer
        // b-blogs konumlandırma
        var blog_wid = $(".b-blog").width() + 6; // bir içeriğin genişliği
        var hmblogs = parseInt(total_wid / blog_wid); // kaç tane sığar
        var total_blogs_wid = blog_wid * hmblogs; // ekrana sığan blog sayısınca olan genişlik
        $(".b-blogs").css({ width: total_blogs_wid });
        // d-detail ayarı
        var detail_wid = (total_wid * 90) / 100; // detail sınıfının genişliği
        $(".d-detail").css("width", detail_wid);

    }

    function wincenter() {
        // nesneleri ekrana ortalar
        // her sayfada sadece 1 tane nesne ortalanabilir
        var body_heig = $("body").height();
        var class_heig = $(".wincenter").height(); // ortalanmak istenen nesneye width değeri verilmeli ardından body 100% olmalı ve wincenter class ismi eklenmeli
        $(".wincenter").css("margin", "auto");
        $(".wincenter").css("margin-top", (body_heig - class_heig) / 2);
        // nesneleri ekrana ortalar
        // ---------
    }

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

    $(".delete").click(function() {
      delete_content(this);
    });
    /* detail delete  */
    $(".d-delete").click(function() {
        delete_content(this);
    });
    //ekran değiştiğinde çalışacak kodlar
    set();
    wincenter();
    $(window).resize(function() {
        set();
        wincenter();
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

    setTimeout(function() {
        $(".main-messages").remove();
        wincenter();//bütün wincenter nesneleri ortalanması için
    }, 3000);


    $(".b-content").mouseover(function() {
        $(this).find(".b-cont").css({
            opacity: "0.1",
        });
        var views = this.getAttribute("data-views");
        var dor = this.getAttribute("data-dor");
        var url = this.getAttribute("data-url");
        var stars = this.getAttribute("data-stars");
        var hmanycomment = this.getAttribute("data-hmanycomment");
        $(this).append("<div class='duread-main'><ul class='duread-ul'><li class='duread-li'><img class='duread-img' src='/static/media/icons/stopwatch.svg'><div class='duread-text'>Tahmini okuma süresi " + dor + " dakika</div></li><li class='duread-li'><img class='duread-img' src='/static/media/icons/star.svg'><div class='duread-text'>Yıldız " + stars + " </div></li><li class='duread-li'><img class='duread-img' src='/static/media/icons/employee.svg'><div class='duread-text'>Okuma " + views + " </div></li><li class='duread-li'><img class='duread-img' src='/static/media/icons/comments.svg'><div class='duread-text'>Yorum sayısı " + hmanycomment + "</div></li></ul></div>");
        $(this).click(function() {
            window.location = "/" + url
        });
    }).mouseout(function() {
        $(this).find(".b-cont").css({
            opacity: "1",
        });
        $(".duread-main").remove();
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
    //users

});
