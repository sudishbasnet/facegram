function myfunction() {
    const url = '/facegram/facegrammer'
    const delay_by_in_ms = 0.5
    let scheduled_function = false

    let ajax_call = function (url, req_param) {
        $.getJSON(url, req_param)
            .done(response => {
                $('#querydata').fadeTo('slow', 0).promise().then(() => {
                    $('#querydata').html(response['html_view'])
                    $('#querydata').fadeTo('slow', 1)
                })
            })
    }

    const req_param = {
        q: $("#searchdata").val()
    }
    //execution cancel if scehduled is false
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    //to retrn id
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, url, req_param)
}