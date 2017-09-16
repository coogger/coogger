(function($) {
    $(document).ready(function() {
        $("#id_fields").change(function() {
            var str = "";
            $("#id_fields option:selected").each(function() {
                str += $(this).val();
                $("#id_branch").load("/chose-branch/" + str);
            });
        });
    });
})(django.jQuery);