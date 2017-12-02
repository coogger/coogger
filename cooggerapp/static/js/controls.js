$(document).ready(function() {
    var str = "";
    $("#id_content_list").each(function() {
        str += $(this).val();
        $(".b-content-list-name a").html("#" + str);
    });

    var str = "";
    $("#id_category option:selected").each(function() {
        str += $(this).val();
        $(".b-category-a").html(str);
    });

    var str = "";
    $("#id_subcategory option:selected").each(function() {
        str += $(this).val();
        $(".b-subcategory-a").html(str);
    });

    var str = "";
    $("#id_category2 option:selected").each(function() {
        str += $(this).val();
        $(".b-category2-a").html(str);
    });

    var str = "";
    $("#id_title").each(function() {
        str += $(this).val();
        $(".b-title-a").html(str);
    });

    var str = "";
    $("#id_show").each(function() {
        str += $(this).val();
        $(".b-content p").html(str);
    });
    // ----------------------------------

    $("#id_content_list").change(function() {
        var str = "";
        $("#id_content_list").each(function() {
            str += $(this).val();
            $(".b-content-list-name a").html("#" + str);
        });
    });

    $("#id_category").change(function() {
        var str = "";
        $("#id_category option:selected").each(function() {
            str += $(this).val();
            $(".b-category-a").html(str);
        });
    });

    $("#id_subcategory").change(function() {
        var str = "";
        $("#id_subcategory option:selected").each(function() {
            str += $(this).val();
            $(".b-subcategory-a").html(str);
        });
    });

    $("#id_category2").change(function() {
        var str = "";
        $("#id_category2 option:selected").each(function() {
            str += $(this).val();
            $(".b-category2-a").html(str);
        });
    });

    $("#id_title").change(function() {
        var str = "";
        $("#id_title").each(function() {
            str += $(this).val();
            $(".b-title-a").html(str);
        });
    });

    $("#id_show").change(function() {
        var str = "";
        $("#id_show").each(function() {
            str += $(this).val();
            $(".b-content p").html(str);
        });
    });
});