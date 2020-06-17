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
        // if($(window).scrollTop() > $("thead").offset().top){
        //     $("thead").css({"position":"fixed","width":$("tbody").width()});
        //     $('thead tr').css({"width":$("tbody").width()});
        //     $('thead tr th').css({"width":$("tbody").width()});
        // }else if($(window).scrollTop() < $("thead").offset().top){
        //     $("thead").css({"position":"absolute"});
        // }
    });
    $(window).resize(function() {
        $(".context").css({
            "left": $('.imager').innerWidth()-parseInt($(".context").css("margin-left")),
            "width":$(window).width()-$(".imager").innerWidth()
        });
    });
});
