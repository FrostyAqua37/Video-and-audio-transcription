"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const buttons = Array.from(document.querySelectorAll('.tab[data-target]'));
    const panels = Array.from(document.querySelectorAll('.panel[role="tabpanel"]'));

    function activateButton(target_id, move_focus = false) {
        buttons.forEach((button) => {
            const is_active = button.dataset.target === target_id;
            button.classList.toggle('is-active', is_active);
            button.setAttribute('aria-selected', String(is_active));
            button.tabIndex = is_active ? 0 : -1;

            if (is_active && move_focus) {
                button.focus();
            }
        });

        panels.forEach((panel) => {
            panel.hidden = panel.id !== target_id;
        });
    }

    buttons.forEach((button, index) => {
        button.addEventListener('click', () => activateButton(button.dataset.target));

        button.addEventListener('keydown', (event) => {
            let next_index;
            switch(event.key) {
                default: 
                    return;

                case 'ArrowRight':
                    next_index = (index + 1) % buttons.length;

                case 'ArrowLeft':
                    next_index = (index - 1 + buttons.length) % buttons.length;

                case 'Home':
                    next_index = 0;
                
                case 'End':
                    next_index = buttons.length - 1;
            };
            
            event.preventDefault();
            activateButton(buttons[next_index].dataset.target, true);
        });
    });

    document.querySelectorAll('input[type="file"]').forEach((input) => {
        input.addEventListener('change', () => {
            const filename = document.getElementById(
                input.id === 'video-upload' ? 'video-filename' : 'audio-filename'
            );

            filename.textContent = input.files && input.files.length ? input.files[0].name : 'No files selected';

        });
    });

    const audio_panel = document.getElementById('audio');
    const video_panel = document.getElementById('video');

    if (audio_panel && audio_panel.querySelector('.media-result')) {
        activateButton('audio');
    } else if (video_panel && video_panel.querySelector('.media-result')) {
        activateButton('video');
    }
});
