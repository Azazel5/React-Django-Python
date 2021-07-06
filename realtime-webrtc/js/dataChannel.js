var localPeerConnection, remotePeerConnection
var sendChannel, receiveChannel

var startButton = document.getElementById("startButton")
var sendButton = document.getElementById("sendButton")
var closeButton = document.getElementById("closeButton")

startButton.disabled = false
sendButton.disabled = true
closeButton.disabled = true

startButton.onclick = createConnection
sendButton.onclick = sendData
closeButton.onclick = closeDataChannels

function createConnection() {
    if (navigator.webkitGetUserMedia)
        RTCPeerConnection = webkitRTCPeerConnection
    else if (navigator.mozGetUserMedia) {
        RTCPeerConnection = mozRTCPeerConnection
        RTCSessionDescription = mozRTCSessionDescription
        RTCIceCandidate = mozRTCIceCandidate
    }

    var servers = null
    var pc_constraints = {
        'optional': [
            { 'DtlsSrtpKeyAgreement': true }
        ]
    }

    localPeerConnection = new RTCPeerConnection(servers, pc_constraints)

    // Creating a data channel with the established localPeerConnection
    try {
        sendChannel = localPeerConnection.createDataChannel("sendDataChannel", { reliable: true })
    } catch (e) {
        alert("Failed to create data channel!")
    }

    localPeerConnection.onicecandidate = gotLocalCandidate
    sendChannel.onopen = handleSendChannelStateChange
    sendChannel.onclose = handleSendChannelStateChange

    window.remotePeerConnection = new RTCPeerConnection(servers, pc_constraints)
    remotePeerConnection.onicecandidate = gotRemoteIceCandidate
    remotePeerConnection.ondatachannel = gotReceiveChannel

    localPeerConnection.createOffer(gotLocalDescription, onSignalingError)

    startButton.disabled = true
    closeButton.disabled = false
}

function onSignalingError(error) {
    console.log("Failed to create signaling message: " + error.name)
}

function sendData() {
    var data = document.getElementById("dataChannelSend").value
    sendChannel.send(data)
}

function closeDataChannels() {
    sendChannel.close()
    receiveChannel.close()
    localPeerConnection.close()
    remotePeerConnection.close()
    localPeerConnection = null
    remotePeerConnection = null

    startButton.disabled = false
    sendButton.disabled = true
    closeButton.disabled = true

    dataChannelSend.value = ""
    dataChannelReceive.value = ""
    dataChannelSend.disabled = true
    dataChannelSend.placeholder = "1: Press Start; 2: Enter text; \
    3: Press Send."
}

function gotLocalDescription(desc) {
    localPeerConnection.setLocalDescription(desc)
    remotePeerConnection.setRemoteDescription(desc)
    remotePeerConnection.createAnswer(gotRemoteDescription, onSignalingError)
}

function gotRemoteDescription(desc) {
    localPeerConnection.setRemoteDescription(desc)
    remotePeerConnection.setLocalDescription(desc)
}

function gotLocalCandidate(event) {
    if (event.candidate)
        remotePeerConnection.addIceCandidate(event.candidate)
}

function gotRemoteIceCandidate(event) {
    if (event.candidate)
        localPeerConnection.addIceCandidate(event.candidate)
}

function gotReceiveChannel(event) {
    receiveChannel = event.channel
    receiveChannel.onopen = handleReceiveChannelStateChange
    receiveChannel.onmessage = handleMessage
    receiveChannel.onclose = handleReceiveChannelStateChange
}

function handleMessage(event) {
    document.getElementById("dataChannelReceive").value = event.data
    document.getElementById("dataChannelSend").value = ""
}

function handleSendChannelStateChange() {
    var readyState = sendChannel.readyState

    if (readyState == "open") {
        dataChannelSend.disabled = false
        dataChannelSend.focus()
        dataChannelSend.placeholder = ""
        sendButton.disabled = false
        closeButton.disabled = false
    }

    else {
        dataChannelSend.disabled = true
        sendButton.disabled = true
        closeButton.disabled = true
    }
}

function handleReceiveChannelStateChange() {
    var readyState = receiveChannel.readyState
    console.log("[handleReceiveChannelStateChange]: readystate: " + readyState)
}