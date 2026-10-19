const buttons = document.querySelector('.buttons'); 
const panels = document.querySelectorAll('.panel');

buttons.addEventListener('click', displaySection);

function displaySection(e) {
    if (e.target.matches('button')) {
        //Makes video and audio button display their respective sections
        const { id } = e.target.dataset;

        if (id == 'video') {
            //Displays video section and highlights button
            showSection(id);
            hideSection('audio');
            activeButton('video-btn');
            unactiveButton('audio-btn');
        }

        if (id == 'audio') {
            //Displays audio section and highlights button
            showSection(id);
            hideSection('video');
            activeButton('audio-btn');
            unactiveButton('video-btn');
        }
    }
}

function showSection(id) {
    document.getElementById(id).style.display = 'block';
}

function hideSection(id) {
    document.getElementById(id).style.display = 'none';
}

function activeButton(id) {
    document.getElementById(id).style.color = '#C4bAA3';
    document.getElementById(id).style.backgroundColor = 'white';
}

function unactiveButton(id) {
    document.getElementById(id).style.color = 'white';
    document.getElementById(id).style.backgroundColor = '#C4bAA3';
}

//Gets the name of uploaded file and displays it.
const upload = document.getElementById('upload');
const filepath = document.getElementById('filepath');

upload.addEventListener('change', function() {
    if (upload.files.length > 0) {
        filepath.textContent = upload.files[0].name;
    }
});
