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
        $(this).append("<div class='duread-main'><ul class='duread-ul'><li class='duread-li'>Tahmini okuma süresi  " + dor + " dakika</li></ul></div>");
    });
    $(".b-content").mouseout(function() {
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
});