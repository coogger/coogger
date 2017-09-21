(function($) {
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
    });
})(django.jQuery);