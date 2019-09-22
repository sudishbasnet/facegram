$(document).on('click', '.addcomment', function (e) {
    e.preventDefault();
    if ($('#content' + e.target.id).val() == '') {
        ('#error' + e.target.id).innerHTML = 'Please enter valid comment';
    }
    else {
        $.ajax({
            type: 'POST',
            url: "/facegram/comment",
            data: {
                content: $('#content' + e.target.id).val(),
                feed: e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (json) {
                $('#content' + e.target.id).val('');
                $('#' + json.post).append(
                    '<div id="cmm' + json.comment + '">' +
                    '<button class="delComment btn-danger col-sm-1" ' + 'id="' + json.comment + '""><i class="fa fa-minus-circle"></i></button>' +
                    "<h5>" +
                    "<a href='/facegram/user/" + json.actorid + "' class='col-sm-2'>" + json.actor + "</a>" +
                    "</h5><h5 class= 'col-sm-9' >" + json.content + "</h5 ></div>");
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});


$(document).on('click', '.savepost', function (e) {
    e.preventDefault();
    const div = '#title' + e.target.id;
    if ($('#title').val() == '') {
        alert("Caption can't be null");
    }
    else {
        $.ajax({
            type: 'POST',
            url: "/facegram/upost",
            data: {
                title: $('#title').val(),
                id: e.target.id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (json) {
                $(div).html(json.title);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }
});


$(document).on('click', '.like-post', function (e) {
    e.preventDefault();
    const div = '#like' + e.target.id;
    $.ajax({
        type: 'POST',
        url: "/facegram/like",
        data: {
            'id': e.target.id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (json) {
            $(div).html("<button type='button' class='like-post btn btn-primary' id=" + json.id + ">" +
                json.like +
                json.span + "<i class='fa fa-heart'></i>" + json.span1);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});



$(document).on('click', '.delComment', function (e) {
    const div = '#cmm' + e.target.id;
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: "/facegram/delComment",
        data: {
            'id': e.target.id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },     // our data object
        success: function (data) {
            $(div).fadeOut(1000);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});


$(document).on('click', '.deleteimg', function (e) {
    const div = '#img' + e.target.id;
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: "/facegram/deleteimg",
        data: {
            'id': e.target.id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },     // our data object
        success: function (data) {
            $(div).html('');

        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});



$(document).on('click', '.delete-post', function (e) {
    const div = '#posts' + e.target.id;
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: "/facegram/delPost",
        data: {
            'id': e.target.id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },     // our data object
        success: function (data) {
            $(div).fadeOut(1000);
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});