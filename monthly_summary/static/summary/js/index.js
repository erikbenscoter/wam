
function inputData(){
  var checkNumber
  var amtPaid
  var monthly_summary

  checkNumber = window.prompt("Please Enter Check Number");
  amtPaid = window.prompt("Please Enter Amt Paid");
  monthly_summary = $("#monthly_summary").val();


  window.location.href="/save_payment/"+checkNumber.toString()+"/"+amtPaid.toString() + "/" +
    monthly_summary.toString().trim();
}

$(".make_payment_button").click(function(){
  inputData();
});
