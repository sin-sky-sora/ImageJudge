$(function(){
    $('.show-btn').css({"bottom":$('.prev-btn').outerHeight()+parseInt($('.prev-btn').css('bottom'))+5});
    $('.window').draggable(true);
    $('.window').css({
      "height":$(".window").height()+$('.window-title').outerHeight(true),
      "text-align":"center",
    });
    $('.window-title span.mini').on('click',function(){
      $(this).parent().next('.canvas-group').animate({"height":"toggle"});
    });
    $('.window-title span.del').on('click',function(){
      $(this).parent().parent("div.window").css({"display":"none"});
    });
});