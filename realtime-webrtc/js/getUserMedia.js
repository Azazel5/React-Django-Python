// Look after different browser vendors' ways of calling the getUserMedia()
// API method:
// Opera --> getUserMedia
// Chrome --> webkitGetUserMedia
// Firefox --> mozGetUserMedia

// Take code from this book with a grain of salt because this is built upon a 
// previous version of WebRTC.

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia
    || navigator.mozGetUserMedia

var vgaButton = document.querySelector("button#vga")
var qvgaButton = document.querySelector("button#qvga")
var hdButton = document.querySelector("button#hd")
var constraints = { audio: false, video: true }
var video = document.querySelector("video")
var st

// Setting any object to the window makes it available to the console for inspection
function successCallback(stream) {
    window.stream = stream
    video.srcObject = stream
    video.play()
}

function errorCallback(error) {
    console.log("navigator.getUserMedia error: ", error)
}

// Constraints object for low resolution video
var qvgaConstraints = {
    video: {
        mandatory: {
            maxWidth: 320,
            maxHeight: 240
        }
    }
}
// Constraints object for standard resolution video
var vgaConstraints = {
    video: {
        mandatory: {
            maxWidth: 640,
            maxHeight: 480
        }
    }
}
// Constraints object for high resolution video
var hdConstraints = {
    video: {
        mandatory: {
            minWidth: 1200,
            minHeight: 600
        }
    }
}

qvgaButton.onclick = function () {
    getMedia(qvgaConstraints)
}

vgaButton.onclick = function () {
    getMedia(vgaConstraints)
}

hdButton.onclick = function () {
    getMedia(hdConstraints)
}

function getMedia(constraints) {
    if (!!st) {
        video.src = null
        st.stop()
    }

    navigator.getUserMedia(constraints, successCallback, errorCallback)
}
