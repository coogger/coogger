$(document).ready(function() {
    function set() {
        var wid = $(window).width();
        if (wid < 607) {
            $("header").css("display", "none");
        } else if {
            $("header").css("display", "block");
        }
    }
    set()
    $(window).resize(function() {
        set();
    });
    $(".open-header").click(function() {
        $("header").toggle("fast");


    });

});