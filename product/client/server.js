const express = require('express');
const path = require('path');
const app = express();

const port = 3000;
const appPath = path.join(__dirname + '/dist');


app.get('/', function(req, res){
  res.sendFile(path.join(appPath + '/index.html'));
});


app.use(express.static(appPath));

app.listen(port);
