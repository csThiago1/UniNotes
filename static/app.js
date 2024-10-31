// Função para obter o token CSRF do HTML (necessária para requisições POST protegidas por CSRF)
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function createNote(color) {
    const content = prompt('Digite o conteúdo da nota:');
    if (content) {
        fetch('/create_note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken() // Adicionando o token CSRF
            },
            body: `content=${encodeURIComponent(content)}&color=${encodeURIComponent(color)}`,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Recarrega a página para mostrar a nova nota
            } else {
                alert(data.error);
            }
        });
    }
}

function editNote(noteId, element) {
    const textarea = element.closest('.note').querySelector('textarea');
    const newContent = prompt('Edite sua nota:', textarea.value);
    if (newContent) {
        fetch(`/edit_note/${noteId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken() // Adicionando o token CSRF
            },
            body: `content=${encodeURIComponent(newContent)}`,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.error);
            }
        });
    }
}

function deleteNote(noteId) {
    if (confirm('Tem certeza que deseja excluir esta nota?')) {
        fetch(`/delete_note/${noteId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken() // Adicionando o token CSRF
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.error);
            }
        });
    }
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('hidden');
}

function logout() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken() // Adicionando o token CSRF
        }
    })
    .then(() => {
        location.reload(); // Recarrega a página após o logout
    });
}
