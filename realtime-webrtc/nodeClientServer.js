var static = require('node-static')
var http = require('http')
var file = new (static.Server)()

var app = http.createServer(function (req, res) {
    file.serve(req, res)
}).listen(8181)

var io = require('socket.io')(app)
io.sockets.on('connection', function (socket) {
    socket.on('message', function (message) {
        console.log('S --> got message: ', message)
        socket.broadcast.to(message.channel).emit('message', message)
    })

    socket.on('create or join', function (room) {
        var numClients = io.sockets.clients(room).length
        log('S --> Room ' + room + ' has ' + numClients + ' client(s)')
        log('S --> Request to create or join room', room)

        if (numClients == 0) {
            socket.join(room)
            socket.emit('created', room)
        } else if (numClients == 1) {
            io.sockets.in(room).emit('join', room)
            socket.join(room)
            socket.emit('joined', room)
        } else {
            socket.emit('full', room)
        }
    })
})

