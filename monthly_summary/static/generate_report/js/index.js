$(document).ready(function(){
  $("#admin").click(function() {
    window.location.href = "/admin"
  });
  $("#root").click(function() {
    window.location.href = "/"
  });
  $("#generate_report").click(function() {

    var username = $("#username").val();
    var month = $("#month").val();
    var year = $("#year").val();

    url = "/report/" + username.toString() + "/" + month.toString() + "/" + year.toString();

    window.location.href = url;
  });

});
