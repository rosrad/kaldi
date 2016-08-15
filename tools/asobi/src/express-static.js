// static.js: serve static files in a directory.
// Ref: http://expressjs.com/api.html#directory

var express = require('express');

var app = express();

app.use(express.logger());
app.use(express.directory('public'));
app.use(express.static('public'));

app.listen(3000);
console.log('Listening on port 3000 ...');
