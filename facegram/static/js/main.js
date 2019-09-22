$('a.toggle-menu').click(function () {
    $(".menu").slideToggle(400);
    return false;
});


$(function () {
    $('[data-rel="lightbox"]').lightbox();
});

