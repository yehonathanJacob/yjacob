function loadTemplate(url, callback) {
    if (templateCache.hasOwnProperty(url)) {
        return Promise.resolve(parseAndLoadTemplate(templateCache[url], callback));
    } else {
        return Promise.resolve($.get('static/' + url, function (data) {
            return parseAndLoadTemplate(data, callback);
        }));
    }
}

function parseAndLoadTemplate(data, callback) {
    data = data.replace(/\n$/, '').replace(/\r\n$/, '');

    var parsed = $.parseHTML(data);
    $.each(parsed, function(index, ele) {
        if(ele.nodeName === 'DIV') {
            var element = $(ele);

            if (callback) {
                callback(element);
            }
        }
    });

    return $.when(parsed);
}
