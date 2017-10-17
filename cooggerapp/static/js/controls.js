$(document).ready(function() {
    var str = "";
    $("#id_content_list").each(function() {
        str += $(this).val();
        $(".blog-content-list-name a").html("#" + str)
    });

    var str = "";
    $("#id_category option:selected").each(function() {
        str += $(this).val();
        $(".blog-category-a").html(str)
    });

    var str = "";
    $("#id_subcategory option:selected").each(function() {
        str += $(this).val();
        $(".blog-subcategory-a").html(str)
    });

    var str = "";
    $("#id_category2 option:selected").each(function() {
        str += $(this).val();
        $(".blog-category2-a").html(str)
    });

    var str = "";
    $("#id_title").each(function() {
        str += $(this).val();
        $(".blog-title-a").html(str)
    });
    // ----------------------------------

    $("#id_content_list").change(function() {
        var str = "";
        $("#id_content_list").each(function() {
            str += $(this).val();
            $(".blog-content-list-name a").html("#" + str)
        });
    });

    $("#id_category").change(function() {
        var str = "";
        $("#id_category option:selected").each(function() {
            str += $(this).val();
            $(".blog-category-a").html(str)
        });
    });

    $("#id_subcategory").change(function() {
        var str = "";
        $("#id_subcategory option:selected").each(function() {
            str += $(this).val();
            $(".blog-subcategory-a").html(str)
        });
    });

    $("#id_category2").change(function() {
        var str = "";
        $("#id_category2 option:selected").each(function() {
            str += $(this).val();
            $(".blog-category2-a").html(str)
        });
    });

    $("#id_title").change(function() {
        var str = "";
        $("#id_title").each(function() {
            str += $(this).val();
            $(".blog-title-a").html(str)
        });
    });
});