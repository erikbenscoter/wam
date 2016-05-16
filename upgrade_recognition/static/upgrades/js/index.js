$(document).ready(function(){
  $('aside').find('.accord').on('click', function(){
    $(this).toggleClass('slide');
    if($(this).hasClass('slide')){
      $(this).next().slideDown(500);
      $(this).css({
        background : '#2C3E50' ,
        color : '#FFFFFF'
      });
      $(this).siblings().next('ul').slideUp(500);
      $(this).siblings().css({
        background : '#FFFFFF' ,
        color : '#2C3E50'
      });
      $(this).children('i').replaceWith('<i class="fa fa-chevron-down pull-right" aria-hidden="true"></i>');
      $(this).siblings('li').find('i').replaceWith('<i class="fa fa-chevron-right pull-right"></i>');
    }
    else {
      $(this).next().slideUp(500);
      $(this).children('i').replaceWith('<i class="fa fa-chevron-right pull-right" aria-hidden="true"></i>');
       $(this).css({
        background : '#FFFFFF' ,
        color : '#2C3E50'
      });
    }
  });
});
