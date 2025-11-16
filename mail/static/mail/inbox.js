console.log("inbox.js działa!");

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archived'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    const composeForm = document.querySelector('#compose-form');
    if (composeForm) composeForm.addEventListener('submit', send_email);

    load_mailbox('inbox');
});

function compose_email() {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';

    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    const emailsView = document.querySelector('#emails-view');
    emailsView.style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/mailbox/${mailbox}/`)
        .then(response => response.json())
        .then(emails => {
            emailsView.innerHTML += emails.length === 0 ? 
                `<p style="margin-top:10px;">Brak maili w tej skrzynce.</p>` : '';

            emails.forEach(email => {
                const div = document.createElement('div');
                div.className = 'email border p-2 mb-2';
                div.dataset.id = email.id;

                console.log(`Email ID: ${email.id}, read =`, email.read);

                if (email.read === true || email.read === "true") {
                    div.classList.add('read-email');
                }

                div.innerHTML = `
                    <span><strong>Od:</strong> ${email.sender}</span> | 
                    <span><strong>Temat:</strong> ${email.subject}</span> | 
                    <span><strong>Data:</strong> ${email.timestamp}</span>
                `;

                div.addEventListener('click', () => open_email(email.id, div, mailbox));

                emailsView.appendChild(div);
            });
        })
        .catch(err => console.error('Błąd ładowania maili:', err));
}

function open_email(email_id, elementDiv, mailbox) {
    console.log('Kliknięto na maila o ID:', email_id);
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    const emailView = document.querySelector('#email-view');
    emailView.style.display = 'block';
    emailView.innerHTML = '<p>Ładowanie...</p>';

    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            console.log('Załadowano maila:', email);

            if (email && email.id) {
                const formattedBody = email.body.split('\n').map((line, index, arr) => {
                    if (line.trim() === '') return '';
                    if (line.startsWith('-----') || line.match(/^\d{4}-\d{2}-\d{2}/) || line.match(/^[\w\.\-]+@[\w\.\-]+/)) {
                        return `<p>${line}</p>`;
                    }
                    if (index > 0 && (arr[index-1].startsWith('-----') || arr[index-1].match(/^\d{4}-\d{2}-\d{2}/) || arr[index-1].match(/^[\w\.\-]+@[\w\.\-]+/))) {
                        return `<p>${line}</p>`;
                    }
                    return `<p><strong>${email.sender} napisał(a):</strong> ${line}</p>`;
                }).join('');

                emailView.innerHTML = `
                    <p><strong>Od:</strong> ${email.sender}</p>
                    <p><strong>Do:</strong> ${email.recipients.join(', ')}</p>
                    <p><strong>Temat:</strong> ${email.subject}</p>
                    <p><strong>Data:</strong> ${email.timestamp}</p>
                    <hr>
                    ${formattedBody}
                    <button id="reply-email-btn">Odpowiedz</button>
                    <button id="archive-email-btn">${email.archived ? 'Przywróć' : 'Archiwizuj'}</button>
                    <button id="close-email-btn">Zamknij</button>
                `;

                document.querySelector('#reply-email-btn').addEventListener('click', () => {
                    compose_email();

                    document.querySelector('#compose-recipients').value = email.sender;

                    let replySubject = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
                    document.querySelector('#compose-subject').value = replySubject;

                    const composeBody = document.querySelector('#compose-body');
                    const userText = '\n\n\n';
                    const quotedText = `----- ${email.timestamp} ${email.sender} napisał(a):\n${email.body}`;

                    composeBody.value = userText + quotedText;

                    composeBody.focus();
                    composeBody.selectionStart = 0;
                    composeBody.selectionEnd = 0;
                });

                // Obsługa archiwizacji/przywracania
                document.querySelector('#archive-email-btn').addEventListener('click', () => {
                    fetch(`/emails/${email.id}/`, {
                        method: 'PUT',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ archived: !email.archived })
                    })
                    .then(() => {
                        // Po zmianie archiwum wracamy do Inbox lub Archived w zależności od kontekstu
                        if (mailbox === 'archived') {
                            load_mailbox('inbox');
                        } else {
                            load_mailbox('inbox');
                        }
                    })
                    .catch(err => console.error('Błąd przy archiwizacji:', err));
                });
            } else {
                console.error('Brak danych maila!');
            }

            if (!email.read) {
                console.log(`Wywołuję PUT dla maila ${email_id}`);
                fetch(`/emails/${email_id}/`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({read: true})
                })
                .then(response => {
                    console.log('Status odpowiedzi PUT:', response.status);
                    return response.json().catch(() => ({}));
                })
                .then(data => {
                    console.log('Odpowiedź PUT:', data);
                    elementDiv.classList.add('read-email');
                    email.read = true;
                })
                .catch(err => console.error('Błąd oznaczania maila jako przeczytany:', err));
            }

            document.querySelector('#close-email-btn').addEventListener('click', () => {
                load_mailbox(mailbox);
            });
        })
        .catch(err => console.error('Błąd ładowania maila:', err));
}

function send_email(event) {
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value.trim();
    const subject = document.querySelector('#compose-subject').value.trim();
    const body = document.querySelector('#compose-body').value.trim();

    // Walidacja treści wiadomości
    if (!body) {
        alert('Treść wiadomości jest wymagana!');
        return;  // Zapobiega wysłaniu pustej wiadomości
    }

    if (!recipients) {
        alert('Musisz podać przynajmniej jednego odbiorcę!');
        return;
    }

    fetch('/emails/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({recipients, subject, body})
    })
    .then(response => {
        if (!response.ok) return response.json().then(err => {throw err});
        return response.json();
    })
    .then(result => {
        console.log('Mail wysłany:', result);
        load_mailbox('sent');
    })
    .catch(err => {
        console.error('Błąd wysyłania:', err);
        alert('Nie udało się wysłać maila: ' + (err.error || JSON.stringify(err)));
    });
}
