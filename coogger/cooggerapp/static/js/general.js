$(document).ready(function() {
    $(".close-ms").click(function() {
        $(".main-messages").remove();
    })
    $(".b-edit-point").click(function() {
        var data_edit_id = this.getAttribute("data-edit-id");
        $(".data-edit-id-" + data_edit_id).toggle("fast");
    });
    $(".lists").click(function() {
        $("nav").toggle("fast");
    });
    $(".fa-arrow-down").click(function() {
        $(".open_header_menu").toggle("fast", function() {});
    });
});
