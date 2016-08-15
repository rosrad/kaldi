/*global $: false, window: false, document: false */
$(function () {
    "use strict";

    var content, input, status, myName, connection, getHourMinute, addMessage,
        addImage, readImageFile, file, sendImage;

    content = $('#content');
    input = $('#input');
    status = $('#status');

    window.WebSocket = window.WebSocket || window.MozWebSocket;

    if (!window.WebSocket) {
        content.html("<p>Sorry, your browser doesn't support WebSocket.</p>");
        input.hide();
        $('span').hide();
        return;
    }

    myName = false;

    connection = new window.WebSocket('ws://127.0.0.1:1337');

    connection.onopen = function () {
        input.removeAttr('disabled');
        status.text('Choose name:');
    };

    connection.onerror = function (error) {
        content.html("<p>Sorry, but there's some problem with your connection or the server is down.");
    };

    connection.onmessage = function (message) {
        var i, json, hist;

        try {
            json = JSON.parse(message.data);
            console.log(json);
        } catch (e) {
            console.log("Invalid JSON: ", message.data);
            return;
        }

        if (json.type === 'welcome') {
            myName = json.name;
            status.text(myName + ': ');
            input.removeAttr('disabled').focus();
        } else if (json.type === 'history') {
            for (i = 0; i < json.data.length; i += 1) {
                hist = json.data[i];
                if (hist.text) {
                    addMessage(hist.author, hist.text, new Date(hist.time));
                } else if (hist.imageSrc) {
                    addImage(hist.author, hist.imageSrc, new Date(hist.time));
                }
            }
        } else if (json.type === 'message') {
            input.removeAttr('disabled');
            addMessage(json.data.author, json.data.text, new Date(json.data.time));
        } else if (json.type === 'image') {
            addImage(json.data.author, json.data.imageSrc, new Date(json.data.time));
        }
    };

    input.keydown(function (e) {
        if (e.keyCode === 13) {
            var msg = $.trim($(this).val());
            if (!msg) {
                return;
            }

            if (!myName) {
                connection.send(JSON.stringify({type: 'hello', name: msg}));
            } else {
                connection.send(JSON.stringify({type: 'message', text: msg}));
            }

            $(this).val('');
            input.attr('disabled', 'disabled');
        }
    });

    setInterval(function () {
        if (connection.readyState !== 1) {
            status.text('Error');
            input.val('Unable to comminucate with the WebSocket server.');
            input.attr('disabled', 'disabled');
        }
    }, 3000);

    getHourMinute = function (dt) {
        return (dt.getHours() < 10 ? '0' + dt.getHours() : dt.getHours()) + ':'
            + (dt.getMinutes() < 10 ? '0' + dt.getMinutes() : dt.getMinutes());
    };

    addMessage = function (author, message, dt) {
        content.prepend('<p><span>' + author + '</span> ' + getHourMinute(dt) + ': ' + message + '</p>');
    };

    addImage = function (author, message, dt) {
        content.prepend('<p><span>' + author + '</span> ' + getHourMinute(dt) + ': ' + '<img src="' + message + '">' + '</p>');
    };

    readImageFile = function (file) {
        var reader = new window.FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (evt) {
            var image = document.getElementById("image");
            image.src = evt.target.result;
        };
    };

    file = document.getElementById("file");
    file.addEventListener("change", function (evt) {
        var file = evt.target.files[0];
        if (file) {
            readImageFile(file);
        }
    });

    sendImage = document.getElementById("send-image");
    sendImage.addEventListener("click", function (evt) {
        var image, imageSrc;
        image = document.getElementById("image");
        imageSrc = image.getAttribute("src");
        connection.send(JSON.stringify({type: 'image', text: imageSrc}));
    });
});
