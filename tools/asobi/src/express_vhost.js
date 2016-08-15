// vhost.js: test the vhost middleware of express.

/*
edit /etc/hosts:

127.0.0.1       foo.example.com
127.0.0.1       bar.example.com
127.0.0.1       example.com
*/

/*
curl http://foo.example.com:3000/
curl http://bar.example.com:3000/
curl http://example.com:3000/
*/

var express = require('express');


// foo.example.com[:3000]
var foo = express();

foo.get('/', function (req, res) {
    res.send('Welcome to foo.example.com!\n');
});


// bar.example.com[:3000]
var bar = express();

bar.get('/', function (req, res) {
    res.send('Welcome to bar.example.com!\n');
});


// Vhost app
var app = express();

app.use(express.logger('dev'));

app.use(express.vhost('foo.example.com', foo));
app.use(express.vhost('bar.example.com', bar));

app.get('*', function(req, res) {
    res.send(404, 'Invalid host!\n');
});


app.listen(3000);
console.log('Listening on port 3000 ...');
