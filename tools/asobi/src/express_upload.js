// upload.js: upload a file.

var fs = require('fs');
var path = require('path');
var express = require('express');

var app = express();

app.use(express.bodyParser());

app.get('/', function (req, res) {
    res.send('<form method="post" enctype="multipart/form-data">'
        + '<p>Image: <input type="file" name="file" /></p>'
        + '<p><input type="submit" value="Upload" /></p>'
        + '</form>');
});

app.post('/', function (req, res, next) {
    // req.files.FOO is <input type="file" name="FOO" />
    var file = req.files.file;

    fs.readFile(file.path, function (err, data) {
        if (err)
            return res.send(500, 'read error: ' + err);

        var savepath = path.join(__dirname, 'upload', file.name);
        fs.writeFile(savepath, data, function (err) {
            if (err)
                return res.send(500, 'write error: ' + err);

            res.send({name: file.name, size: file.size});
        });
    });
});

app.listen(3000);
console.log('Listening on port 3000 ...');
