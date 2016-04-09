
function inputData(){
  var checkNumber
  var amtPaid
  

  checkNumber = window.prompt("Please Enter Check Number");
  amtPaid = window.prompt("Please Enter Amt Paid");
  
  var getParameters = "?checkNumber="+checkNumber.toString()+"&amtPaid="+amtPaid.toString();
  
  window.location.href="/savePaymentInput/"+getParameters;
}

$(".make_payment_button").click(function(){
  inputData();
});