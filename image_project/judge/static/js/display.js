$(function(){
    $(".imager").css({
        "position":"fixed",
        "left":0,
        "top":$(".content").offset().top
    });
    $('.context').css({
        "left":$('.imager').innerWidth()-parseInt($(".context").css("margin-left")),
        "width":$(window).width()-$(".imager").innerWidth()
    });
    $('.prev-btn').css({"position":"fixed","left":5,"bottom":5});
    $(window).on("scroll", function() {
          ;//メニュー開閉
    });
    $(window).resize(function() {
        $(".context").css({
            "left": $('.imager').innerWidth()-parseInt($(".context").css("margin-left")),
            "width":$(window).width()-$(".imager").innerWidth()
        });
    });
});
