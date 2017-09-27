$(document).ready(function() {
    $("header").mouseover(function() {
        $(".uploadform").css({ display: "block" });
    }).mouseout(function() {
        $(".uploadform").css({ display: "none" });
    });
    $(".close-ms").click(function() {
        $(".main-messages").remove();
    })
});