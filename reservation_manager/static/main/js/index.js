var owner;
var resort;
var unit_size;
var traveler;
var upgrades;
var in_days;

function getAllFilterValues() {
  owner = $("#owner_filter").val();
  resort = $("#resort_filter").val();
  unit_size = $("#unit_size_filter").val();
  traveler = $("#traveler_filter").val();
  upgrades = $("#upgrades_filter").val();
  in_days = $("#days_filter").val();
  if(in_days == ""){
    in_days = -1
  }else {
    int_days = parseInt(in_days);
  }

}

function showAllRows(){
  $("tr").show();
}

function showAllRowsThatMatchFilter() {
  $("tr").not(":first").each(function(){

    if(owner != "---"){
      var row_owner = $(this).children(".username").html();
      if(row_owner != owner){
        $(this).hide();
      }
    }

    if(resort != "---"){
      var row_resort = $(this).children(".location").html();
      if(row_resort != resort){
        $(this).hide();
      }
    }

    if(unit_size != "---"){
      var row_unit_size = $(this).children(".size").html();
      if(row_unit_size != unit_size){
        $(this).hide();
      }
    }

    if(traveler != "---"){
      var row_traveler = $(this).children(".traveler").html();
      if(row_traveler != traveler){
        $(this).hide();
      }
    }

    if(upgrades != "---"){
      var row_upgrades = $(this).children(".upgrade").html();
      if(row_upgrades != upgrades){
        $(this).hide();
      }
    }

    if( in_days != -1 ){
      var today = new Date();
      var row_checkin = $(this).children(".checkin").html();
      var row_checkin = new Date(row_checkin);
      var diff = row_checkin - today;
      diff = parseInt( diff / (1000 * 3600 * 24) );

      if ( in_days - diff < 0){
        $(this).hide();
      }
    }

  });
}

function countMatchingRows() {
  total = 0;
  $("tr:visible").each(function(){
    total++;
  });
  total--; //subtract the heading
  $("#num_match").html(total);
}

function updateTable() {
  getAllFilterValues();
  showAllRows();
  showAllRowsThatMatchFilter();
  countMatchingRows();
}

$("#btn_apply_filter").click(function(){
  updateTable();
});

$("input").change(function(){
  updateTable();
});

$("select").change(function(){
  updateTable();
});

updateTable();
