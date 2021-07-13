'use strict'

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia

window.onbeforeunload = function (e) {
    hangup()
}

var sendChannel, receiveChannel
var sendButton = document.getElementById("sendButton")
var sendTextarea = document.getElementById("dataChannelSend")
var receiveTextarea = document.getElementById("dataChannelReceive")

var localVideo = document.querySelector('#localVideo')
var remoteVideo = document.querySelector('#remoteVideo')

sendButton.click = sendData

var isChannelReady = false
var isInitiator = false
var isStarted = false

var localStream
var remoteStream

var pc

// STUN and TURN servers 
var pcConfig = { 'iceServers': [{ 'url': 'stun:stun.l.google.com:19302' }] }

var pcConstraints = {
    'optional': [
        { 'DtlsSrtpKeyAgreement': true }
    ]
}

var sdpConstraints = {}
var room = prompt('Enter room name: ')
var socket = io.connect('http://localhost:8181', { transports: ['websocket'] })

if (room == "") {
    console.log('Create or join room', room)
    socket.emit('create or join', room)
}

var constraints = { video: true, audio: true }

function handleUserMedia(stream) {
    localStream = stream
    attachMediaStream(localVideo, stream)
    console.log('Adding local stream')
    sendMessage('got user media')
}

function handleUserMediaError(error) {
    console.log('navigator.getUserMedia error: ', error);
}

socket.on('created', function (room) {
    console.log('Created room ' + room)
    isInitiator = true
    navigator.getUserMedia(constraints, handleUserMedia, handleUserMediaError)
    console.log('Getting user media with constraints', constraints)
    checkAndStart()
})

socket.on('full', function (room) {
    console.log('Room ' + room + ' is full')
})

socket.on('join', function (room) {
    console.log('Another peer made a request to join room ' + room)
    console.log('This peer is the initiator of room ' + room + '!')
    isChannelReady = true
})

socket.on('joined', function (room) {
    console.log('This peer has joined room ' + room)
    isChannelReady = true
    navigator.getUserMedia(constraints, handleUserMedia, handleUserMediaError)
    console.log('Getting user media with constraints', constraints)
})

socket.on('log', function (array) {
    console.log.apply(console, array)
})

socket.on('message', function (message) {
    console.log('Received message: ', message)
    if (message === 'got user media') {
        checkAndStart()
    } else if (message.type === 'offer') {
        if (!isInitiator && !isStarted) {
            checkAndStart()
        }

        pc.setRemoteDescription(new RTCSessionDescription(message))
        doAnswer()
    } else if (message.type === 'answer' && isStarted) {
        pc.setRemoteDescription(new RTCSessionDescription(message))
    } else if (message.type === 'candidate' && isStarted) {
        var candidate = new RTCIceCandidate({
            sdpMLineIndex: message.label,
            candidate: message.candidate
        })
        pc.addIceCandidate(candidate)
    } else if (message === 'bye' && isStarted) {
        hadnleRemoteHangup()
    }
})

function sendMessage(message) {
    socket.emit('message', message)
}

function checkAndStart() {
    if (!isStarted && typeof localStream != 'undefined' && isChannelReady) {
        createPeerConnection()
        isStarted = true
        if (isInitiator) {
            doCall()
        }
    }
}

function createPeerConnection() {
    try {
        pc = new RTCPeerConnection(pcConfig, pcConstraints)
        pc.addStream(localStream)
        pc.onicecandidate = handleIceCandidate
    } catch (e) {
        alert('Cannot create RTCPeerConnection')
        return
    }

    pc.onaddstream = handleRemoteStreamAdded
    pc.onremovestream = handleRemoteStreamRemoved

    if (isInitiator) {
        try {
            sendChannel = pc.createDataChannel('sendDataChannel', {
                reliable: true
            })
        } catch (e) {
            alert('Failed to create data channel')
        }

        sendChannel.onopen = handleSendChannelStateChange
        sendChannel.onclose = handleSendChannelStateChange
        sendChannel.onmessgage = handleMessage
    } else {
        // The joiner
        pc.ondatachannel = gotReceiveChannel
    }
}

function sendData() {
    var data = sendTextarea.value
    if (isInitiator)
        sendChannel.send(data)
    else
        receiveChannel.send(data)
}

/** Here's a big bunch of handlers */
function gotReceiveChannel(event) {
    receiveChannel = event.channel
    receiveChannel.onmessage = handleMessage
    receiveChannel.onopen = handleReceiveChannelStateChange
    receiveChannel.onclose = handleReceiveChannelStateChange
}

function handleMessage(event) {
    receiveTextarea.value += event.data + '\n'
}

function handleSendChannelStateChange() {
    var readyState = sendChannel.readyState
    if (readyState == 'open') {
        sendTextarea.disabled = false
        sendTextarea.focus()
        sendTextarea.placeholder = ''
        sendButton.disabled = false
    } else {
        sendTextarea.disabled = true
        sendButton.disabled = true
    }
}

function handleReceiveChannelStateChange() {
    var readyState = receiveChannel.readyState
    if (readyState == 'open') {
        sendTextarea.disabled = false
        sendTextarea.focus()
        sendTextarea.placeholder = ''
        sendButton.disabled = false
    } else {
        sendTextarea.disabled = true
        sendButton.disabled = true
    }
}

function handleIceCandidate(event) {
    if (event.candidate) {
        sendMessage({
            type: 'candidate',
            label: event.candidate.sdpMLineIndex,
            id: event.candidate.sdpMid,
            candidate: event.candidate.candidate
        })
    } else
        console.log('Done with candidates')
}

function doCall() {
    pc.createOffer(setLocalAndSendMessage, onSignalingError, sdpConstraints)
}

function onSignalingError(error) {
    console.log('Failed to create signaling message : ' + error.name);
}

function doAnswer() {
    pc.createAnswer(setLocalAndSendMessage, onSignalingError, sdpConstraints)
}

function setLocalAndSendMessage(sessionDescription) {
    pc.setLocalDescription(sessionDescription)
    sendMessage(sessionDescription)
}

function handleRemoteStreamAdded(event) {
    attachMediaStream(remoteVideo, event.stream)
    remoteStream = event.stream
}

function handleRemoteStreamRemoved(event) {
    console.log('Remote stream removed')
}

function hangup() {
    stop()
    sendMessage('bye')
}

function hadnleRemoteHangup() {
    stop()
    isInitiator = false
}

function stop() {
    isStarted = false
    if (sendChannel) sendChannel.close()
    if (receiveChannel) receiveChannel.close()
    if (pc) pc.close()
    pc = null
    sendButton.disabled = true
}