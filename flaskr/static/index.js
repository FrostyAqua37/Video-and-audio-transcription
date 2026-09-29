async function getSubtitles() {
    try {
        const response = await fetch('./subtitles.json');

        if (!response.ok) {
            throw new Error(`Error! Status; ${response.status}`);
        }

        const data = await response.json();
        
        console.log(data);
    } catch (error) {
        console.log(error);
    }
}

/*
getSubtitles().then(data => {
    console.log(data);

    const ul = document.createElement('ul');

    data.forEach(subtitle => {
        const li = document.createElement('li');
        li.innerHTML = li.text;
        li.style.fontSize = '22px';
    }) */

getSubtitles();