// app.js: A nodejs web app demo.
//
// package.json
// {
//   "name": "online",
//   "description": "simple online counter app",
//   "version": "0.0.1",
//   "private": true,
//   "dependencies": {
//     "express": "3.x",
//     "redis": "*"
//   }
// }
//
// Ref: http://expressjs.com/guide.html#users-online


var express = require('express');
var redis = require('redis');
var db = redis.createClient();
var app = express();

app.use(function (req, res, next) {
    var ua = req.headers['user-agent'];
    db.zadd('online', Date.now(), ua, next);
});

app.use(function (req, res, next) {
    var min = 60 * 1000;
    var ago = Date.now() - min;  // one minute ago
    db.zrevrangebyscore('online', '+inf', ago, function (err, users) {
        if (err)
            return next(err);

        req.online = users;
        next();
    });
});

app.get('/', function (req, res) {
    res.send(req.online.length + ' users online');
});

app.listen(3000);
console.log('Listening on port 3000 ...');
