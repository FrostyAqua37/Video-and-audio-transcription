(function mediaPlayer() {
    var URL = window.URL || window.webkitURL
    var message = function(title, error) {
        var element = document.querySelector("#title")
        element.innerHTML = title
        element.className = error ? "error" : "info"
    }

    var displayMedia = function(event) {
        var file = this.files[0]
        var type = file.type
        var videoDisplay = document.querySelector("video")
        var canPlay = videoDisplay.canPlayType(type)

        if (canPlay == "") canPlay = false
        var title = file.title
        var error = canPlay == false

        message(title, error)

        if (error) {
            return
        }

        var fileURL = URL.createObjectURL(file)
        videoDisplay.src = fileURL
    }
    var input = document.querySelector("input")
    input.addEventListener("change", displayMedia, false)
})()