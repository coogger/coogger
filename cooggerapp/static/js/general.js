$(document).ready(function() {
    function set() {
        var wid = parseInt($(window).width());
        var heig = parseInt($(window).height());
        if (wid < 1160) {
            var nav_wid = 0;
        } else {
            var nav_wid = parseInt($("nav").width() + 24);
        }
        var blog_wid = parseInt($(".b-blog").width() + 12); // bir içeriğin genişliği
        var total_wid = parseInt(wid - nav_wid); // ekranda boş kalan yer
        var hmblogs = parseInt(total_wid / (blog_wid)); // kaç tane sığar
        var total_blogs_wid = parseInt(blog_wid * hmblogs); // ekrana sığan blog sayısınca olan genişlik
        var pagi_wid = parseInt($(".pagination").width()); // pagination sınıfının genişliği
        // footer
        $("footer").css({ width: wid - nav_wid });
        // blogs konumlandırma
        var hmany_blogs = parseInt();
        $(".blogs").css({ width: total_blogs_wid });
        $(".blogs").css("margin-left", (wid - total_blogs_wid + nav_wid) / 2);
        // paginator konumlandırma
        $(".pagination").css("margin-left", (total_wid - pagi_wid) / 2 + nav_wid);
        // nav yükseklik ayarı
        $(".main-nav").css("height", heig - 120);
        // detail ayarı
        var detail_wid = parseInt((total_wid * 90) / 100); // detail sınıfının genişliği
        if (wid > 1160) {
            $(".datail").css("margin-right", (total_wid - detail_wid) / 2);
        }
        $(".datail").css("width", detail_wid);

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

    var wid = parseInt($(window).width());
    if (wid < 1160) { // mobil ve tablet
        $(".header-ul").addClass("wincenter");
        $(".open-header").click(function() {
            $("header").toggle("fast")
        });
    }

    //ekran değiştiğinde çalışacak kodlar
    set();
    wincenter();
    $(window).resize(function() {
        set();
        wincenter();
    });

    // her zaman çalışacak kodlar
    $(".close-ms").click(function() {
        $(".main-messages").remove();
    })
    setTimeout(function() {
        $(".main-messages").remove();
    }, 3000);
    $(".b-content").mouseover(function() {
        $(this).find(".blog-cont").css({
            filter: "blur(3px)",
        });
        var dor = this.getAttribute("data-dor");
        var url = this.getAttribute("data-url");
        var stars = this.getAttribute("data-stars");
        $(this).append("<div class='duread-main'><ul class='duread-ul'><li class='duread-li'>Tahmini okuma süresi " + dor + " dakika</li><li class='duread-li'>yıldızlar " + stars + " </li></ul></div>");
        $(this).click(function() {
            window.location = "/" + url
        });
    }).mouseout(function() {
        $(".blog-cont").css({
            filter: "blur(0px)",
        });
        $(".duread-main").remove();
    });
    $(".delete").click(function() {
        var conf = confirm("Silmek istediğinize eminmisiniz ! bu işlem geri alınamaz");
        if (conf) {
            var delete_id = this.getAttribute("data-delete-id");
            $(".error").load("/delete/" + delete_id);
            $(".main-messages").css({ display: "block" });
            $(".id-" + delete_id).remove();
        }
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
        $(".uploadform").css({ display: "block" });
    }).mouseout(function() {
        $(".uploadform").css({ display: "none" });
    });
    //users
});