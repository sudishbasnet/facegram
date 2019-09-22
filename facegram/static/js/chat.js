const msgbox = '<div class="msg right" style="background-color:gray;">' +
    '<div style="position: absolute;"><h5>{sender}</h5></div><br>' +
    '{message}<br><br>' +
    '</div>';

let userState = ''

const userDiv = (senderId, receiverId,photo, name) =>
    (`<a href="/chat/${senderId}/${receiverId}" id="user${receiverId}">
                    <img src="${photo}" style="width:80px;height:80px;border-radius:100%;margin:0 10px 0 10px"><br>
                    <span>${name}</span><br>
    </a>`)

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    $.post('/api/messages', '{"sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }', function (data) {
        var box = msgbox.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/api/messages/' + sender_id + '/' + receiver_id, function (data) {
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                var box = msgbox.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left bg-primary');
                box = box.replace('background-color:gray','');
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}

function getUsers(senderId, callback) {
    return $.get('/api/users', function (data) {
        if (userState !== JSON.stringify(data)) {
            userState = JSON.stringify(data);
            const doc = data.reduce((res, user) => {
                if (user.id === senderId) {
                    return res
                } else {
                    return [userDiv(senderId, user.id, user.photo, user.username), ...res]
                }
            }, [])
            callback(doc)
        }
    })
}

