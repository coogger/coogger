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
    $(window).resize(function() {
        set();
    });

    $(".open-header").click(function() {

        $("header").toggle("fast");


    });

});