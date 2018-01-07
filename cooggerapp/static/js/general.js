$(document).ready(function() {
  function delete_content(this_){//içerik silmek için
        var conf = confirm("Silmek istediğinize eminmisiniz ! bu işlem geri alınamaz");
        if (conf) {
            var delete_id = this_.getAttribute("data-post-id");
            $(".wms").load("/delete/"+delete_id);
            $(".main-messages").css({ display: "block" });
            $(".data-post-id-" + delete_id).remove();
            setTimeout(function() {
                $(".main-messages").css({ display: "none" });
            }, 3000);
        }
      }

      $(".delete").click(function() {
        delete_content(this);
  });

    // her zaman çalışacak kodlar
    $(".close-ms").click(function() {
        $(".main-messages").remove();
    })

    $(".b-edit-point").click(function() {
        var data_edit_id = this.getAttribute("data-edit-id");
        $(".data-edit-id-" + data_edit_id).toggle("fast");
    });

});
