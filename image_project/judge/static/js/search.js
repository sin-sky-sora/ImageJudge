$(function(){
    /* 検索 */
    $('div.menu ul li label input.search-item').change(function(){
        $('.model-name').parent('tr').addClass("hide");
        var target = $('input.search-item:checked').length;
        if(!target)
            $('.model-name').parent('tr').removeClass("hide");
        else{
            $('.search-item:checked').each(function(){
                var r = $(this).val();
                $('.model-name').each(function(){
                    var k = $(this).data('value');
                    k = String(k).split(" ");
                    k.forEach((item) => {
                    if(item == r)
                        $(this).parent('tr').removeClass('hide');
                    });
                });
            });
        }
    });
    /* トグル */
    $('.toggle').on('click',function(){
        $(this).parent().next("ul.menu-custom").animate({"height":"toggle"});
    });
    /* ドラッグを可能に */
    $('.menu').draggable(true);
    $('.menu').css({
        "width":$(".menu").width()
    });
})