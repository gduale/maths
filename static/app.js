document.querySelectorAll('[data-open-dialog]').forEach(button => button.addEventListener('click', () => document.getElementById(button.dataset.openDialog).showModal()));
document.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
const dialog = document.querySelector('#profile-dialog');
document.querySelector('[data-open-profile]')?.addEventListener('click', () => dialog.showModal());
document.querySelector('[data-close-profile]')?.addEventListener('click', () => dialog.close());
const answer = document.querySelector('#answer');
const check = document.querySelector('#check-answer');
function update(value) { if (!check) return; answer.value = value; check.disabled = !value.length; }
document.querySelectorAll('[data-digit]').forEach(button => button.addEventListener('click', () => { if (answer.value.length < 3) update((answer.value === '0' ? '' : answer.value) + button.dataset.digit); }));
document.querySelector('[data-erase]')?.addEventListener('click', () => update(answer.value.slice(0, -1)));
document.addEventListener('keydown', event => { if (!check) return; if (/^[0-9]$/.test(event.key)) { event.preventDefault(); if (answer.value.length < 3) update((answer.value === '0' ? '' : answer.value) + event.key); } else if (event.key === 'Backspace') { event.preventDefault(); update(answer.value.slice(0, -1)); } });
