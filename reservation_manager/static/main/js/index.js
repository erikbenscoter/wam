var owner;
var resort;
var unit_size;
var traveler;
var upgrades;
var show_cancelations;
var in_days;

var cb_Owner;
var cb_Conf;
var cb_Checkin;
var cb_Nights;
var cb_Resort;
var cb_Unit;
var cb_Booked;
var cb_Traveler;
var cb_Upgrade;
var cb_Points;

function getCheckboxes(){
  var checkboxes = [
    "#cb_Owner",
    "#cb_Conf",
    "#cb_Checkin",
    "#cb_Nights",
    "#cb_Resort",
    "#cb_Unit",
    "#cb_Booked",
    "#cb_Traveler",
    "#cb_Upgrade",
    "#cb_Points",
  ]

  var column_classes = [
    ".username",
    ".conf",
    ".checkin",
    ".nights",
    ".location",
    ".size",
    ".booked",
    ".traveler",
    ".upgrade",
    ".points"
  ]


  for (var i = 0; i < column_classes.length; i++) {
    if ($(checkboxes[i]).prop("checked")) {
      $(column_classes[i]).show();
      $(checkboxes[i]).parent().removeClass("pink");
    }else{
      $(column_classes[i]).hide();
      $(checkboxes[i]).parent().addClass("pink");
    }
  }















}



function getAllFilterValues() {
  owner = $("#owner_filter").val();
  resort = $("#resort_filter").val();
  unit_size = $("#unit_size_filter").val();
  traveler = $("#traveler_filter").val();
  upgrades = $("#upgrades_filter").val();
  in_days = $("#days_filter").val();
  show_cancelations = $("#cancelations_filter").val();

  show_cancelations = parseInt(show_cancelations)
  if(in_days == ""){
    in_days = -1
  }else {
    int_days = parseInt(in_days);
  }

  if(show_cancelations == 0){
    show_cancelations = false;
  }else{
    show_cancelations = true;
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

    if(show_cancelations == false){
      var is_canceled_row = $(this).hasClass("canceled")
      if(is_canceled_row){
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
  getCheckboxes();
});

$("select").change(function(){
  updateTable();
});

updateTable();
