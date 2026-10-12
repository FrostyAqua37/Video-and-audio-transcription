const buttons = document.querySelector('.buttons');
const panels = document.querySelectorAll('.panel');

buttons.addEventListener('click', displaySection);

function displaySection(e) {
    if (e.target.matches('button')) {
        //panels.forEach(panel => panel.classList.add('hide')); 

        const { id } = e.target.dataset;
        const selector = `.panel[id="${id}"]`;

        style = getStyleValues(id);
        changeDisplay(id, style.getPropertyValue('display'));
        //document.querySelector(selector).classList.remove('hide');
    }
}

function getStyleValues(id) {
    let element = document.getElementById(id);
    return window.getComputedStyle(element);
}

function changeDisplay(id, value) {
    if (value == 'block') {
        document.getElementById(id).style.display = 'none';
    } else if (value == 'none') {
        document.getElementById(id).style.display = 'block';
    }
}