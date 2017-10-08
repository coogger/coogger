$(document).ready(function() {
    function set() {
        var wid = $(window).width();
        if (wid > 48 && wid < 687) {
            $(".main-blog-cards").css({ width: "306px" });
        }
        if (wid > 686 && wid < 1028) {
            $(".main-blog-cards").css({ width: "612px" });
        }
        if (wid > 1027 && wid < 1369) {
            $(".main-blog-cards").css({ width: "918px" });
        }
        if (wid > 1368 && wid < 1710) {
            $(".main-blog-cards").css({ width: "1224px" });
        }
        if (wid > 1709 && wid < 2051) {
            $(".main-blog-cards").css({ width: "1530px" });
        }

        if (wid < 607) {
            $("header").css("display", "none");
        } else {
            $("header").css("display", "block");
        }
    }

    set();
    var wid = $(window).width();
    var heig = $(window).height();
    if (wid > 769) { // mobil değil ise
        $(window).resize(function() {
            set();
        });
    } else { // mobil ise
        $(".open-header").click(function() {
            $("header").toggle("fast");
        });
    }
    // her zaman
    $(".close-ms").click(function() {
        $(".main-messages").remove();
    })
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
    // nesneleri ekrana ortalar
    // her sayfada sadece 1 tane nesne ortalanabilir
    var body_heig = $("body").height();
    var class_heig = $(".wincenter").height(); // ortalanmak istenen nesneye width değeri verilmeli ardından body 100% olmalı ve wincenter class ismi eklenmeli
    $(".wincenter").css("margin", "auto");
    $(".wincenter").css("margin-top", (body_heig - class_heig) / 2);
    // nesneleri ekrana ortalar
    // ---------
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