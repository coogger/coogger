$(document).ready(function() {
  function editor_change(){
        $("#id_content_list").each(function() {
          var str = "";
            str += $(this).val();
            $(".list-name").html(str);
        });

        $("#id_title").each(function() {
          var str = "";
            str += $(this).val();
            $(".title").html(str);
        });

        $("#id_show").each(function() {
          var str = "";
            str += $(this).val();
            $(".show").html(str);
        });


        $("#id_tag").each(function() {
          var str = "";
            str += $(this).val();
            str = new String(str);
            str = str.split(",");
            var tag = "";
            for (i=0; i < str.length; i++) {
              if (str[i] != ""){
                tag += '<li class="tag" default="pm" hvr="c-success" flx="" gnrl="c-muted bg-dark br-3">'+str[i]+'</li>'
              }
            }
            $(".tags").html(tag);
        });

        $("#id_content_list").each(function() {
          var str = "";
            str += $(this).val();
            str = new String(str);
            if (str != ""){
                str = '<li class="tag" default="pm" hvr="c-success" flx="" gnrl="c-muted bg-dark br-3">'+str+'</li>'
            }
            $(".list").html(str );
        });

        }

 setInterval(function(){
    editor_change();
  },100);


});
