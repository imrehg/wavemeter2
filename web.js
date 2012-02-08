require.paths.unshift(__dirname + '/lib');

var express = require('express');
var uuid = require('node-uuid');

var app = express.createServer(express.logger());

// create a socket.io backend for sending facebook graph data
// to the browser as we receive it
var io = require('socket.io').listen(app);

// use xhr-polling as the transport for socket.io
io.configure(function () {
  io.set("transports", ["xhr-polling"]);
  io.set("polling duration", 10);
});

app.get('/', function(request, response) {

  var method = request.headers['x-forwarded-proto'] || 'http';
  var socket_id = uuid();

  response.render('home.ejs', {
          layout:   false,
          app:      app,
          home:     method + '://' + request.headers.host + '/',
          redirect: method + '://' + request.headers.host + request.url,
          socket_id: socket_id
        });
});

var port = process.env.PORT || 3000;
app.listen(port, function() {
  console.log("Listening on " + port);
});
