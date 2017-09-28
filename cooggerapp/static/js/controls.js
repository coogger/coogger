$(document).ready(function() {
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

    $(".delete").click(function() {
        var conf = confirm("Silmek istediğinize eminmisiniz ! bu işlem geri alınamaz");
        if (conf) {
            var delete_id = this.getAttribute("data-delete-id");
            $(".error").load("/delete/" + delete_id);
            $(".main-messages").css({ display: "block" });
            $(".id-" + delete_id).remove();
        }
    });
    $(".close-ms").click(function() {
        $(".main-messages").remove();
    })
});