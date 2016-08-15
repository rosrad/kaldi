// Refer to:
// http://martinsikora.com/nodejs-and-websocket-simple-chat-tutorial
// https://gist.github.com/martinsik/2031681

// http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/
"use strict";

// Optional. You will see this name in eg. 'ps' or 'top' command
process.title = 'node-chat';

var http, WebSocketServer,
    webSocketsServerPort, history, clients, server, wsServer,
    htmlEntities;

// Port where we'll run the websocket server
webSocketsServerPort = 1337;

// npm install websocket
WebSocketServer = require('websocket').server;
http = require('http');

// latest 100 messages
history = [];
// list of currently connected clients (users)
clients = [];

// Helper function for escaping input strings
htmlEntities = function (str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
};

// HTTP server
server = http.createServer(function (request, response) {
    // Not important for us. We're writing WebSocket server, not HTTP server
});

server.listen(webSocketsServerPort, function () {
    console.log((new Date()) + " Server is listening on port " + webSocketsServerPort);
});

// WebSocket server
wsServer = new WebSocketServer({
    // WebSocket server is tied to a HTTP server. WebSocket request is just
    // an enhanced HTTP request. For more info http://tools.ietf.org/html/rfc6455#page-6
    httpServer: server
});

// This callback function is called every time someone
// tries to connect to the WebSocket server
wsServer.on('request', function (request) {
    var connection, index, userName;

    console.log((new Date()) + ' Connection from origin ' + request.origin + '.');

    // accept connection - you should check 'request.origin' to make sure that
    // client is connecting from your website
    // (http://en.wikipedia.org/wiki/Same_origin_policy)
    connection = request.accept(null, request.origin);
    // we need to know client index to remove them on 'close' event
    index = clients.push(connection) - 1;
    userName = false;

    console.log((new Date()) + ' Connection accepted.');

    // send back chat history
    if (history.length > 0) {
        connection.sendUTF(JSON.stringify({type: 'history', data: history}));
    }

    // user sent some message
    connection.on('message', function (message) {
        var i, json, obj;

        if (message.type === 'utf8') { // accept only text
            json = JSON.parse(message.utf8Data);
            console.log(json);
            if (json.type === 'hello') {
                userName = htmlEntities(json.name);
                connection.sendUTF(JSON.stringify({type: 'welcome', name: userName}));
                console.log((new Date()) + ' User is known as: ' + userName);
            } else if (json.type === 'message') {
                console.log((new Date()) + ' Received Message from ' + userName + ': ' + json.text);
                obj = {
                    time: (new Date()).getTime(),
                    text: htmlEntities(json.text),
                    author: userName
                };
                history.push(obj);
                history = history.slice(-100);

                // broadcast message to all connected clients
                json = JSON.stringify({type: 'message', data: obj});
                for (i = 0; i < clients.length; i += 1) {
                    clients[i].sendUTF(json);
                }
            } else if (json.type === 'image') {
                obj = {
                    time: (new Date()).getTime(),
                    imageSrc: json.text,
                    author: userName
                };
                history.push(obj);
                history = history.slice(-100);

                // broadcast message to all connected clients
                json = JSON.stringify({type: 'image', data: obj});
                for (i = 0; i < clients.length; i += 1) {
                    clients[i].sendUTF(json);
                }
            }
        }
    });

    // user disconnected
    connection.on('close', function (connection) {
        if (userName !== false) {
            console.log((new Date()) + " Peer " + userName + " disconnected.");
            // remove user from the list of connected clients
            clients.splice(index, 1);
        }
    });
});
