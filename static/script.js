function pegar_nome_usuario() {
    return localStorage.getItem('nome_usuario') || '';
}

function definir_nome_usuario(nome) {
    localStorage.setItem('nome_usuario', nome);
}

function pegar_lembretes() {
    const dados = localStorage.getItem('lembretes');
    return dados ? JSON.parse(dados) : [];
}

function salvar_lembretes(lembretes) {
    localStorage.setItem('lembretes', JSON.stringify(lembretes));
}

function criar_lembrete(titulo, detalhes) {
    const lembretes = pegar_lembretes();
    lembretes.push({
        id: Date.now(),
        titulo: titulo.trim(),
        detalhes: detalhes.trim(),
        criado_em: new Date().toISOString()
    });
    salvar_lembretes(lembretes);
}

function excluir_lembrete(id) {
    const lembretes = pegar_lembretes().filter(item => item.id !== id);
    salvar_lembretes(lembretes);
}

function mostrar_pagina_inicial() {
    console.log('mostrar_pagina_inicial chamada');
    const subtitulo = document.getElementById('mensagem_subtitulo');
    const sem_lembretes = document.getElementById('sem_lembretes');
    const lista_lembretes = document.getElementById('lista_lembretes');
    const container_lembretes = document.getElementById('lembretes');

    const lembretes = pegar_lembretes();
    console.log('Lembretes encontrados:', lembretes.length, lembretes);
    if (!lembretes.length){
        subtitulo.textContent = "Você ainda não tem lembretes.";
        sem_lembretes.classList.remove('hidden');
        lista_lembretes.classList.add('hidden');
        container_lembretes.innerHTML = '';
        return;
    }
    subtitulo.textContent = "Lembretes recentes:";
    sem_lembretes.classList.add('hidden');
    lista_lembretes.classList.remove('hidden');

    container_lembretes.innerHTML = lembretes.map(lembrete => `
        <article class="lembrete">
            <div>
                <h2>${lembrete.titulo}</h2>
                <p>${lembrete.detalhes}</p>
            </div>
            <div class="acoes_lembrete">
                <a class="botao secundario" href="/editar?id=${lembrete.id}">Editar</a>
                <button class="botao perigo" data-id="${lembrete.id}">Excluir</button>
            </div>
        </article>
    `).join('');

    container_lembretes.querySelectorAll('button[data-id]').forEach(button => {
        button.addEventListener('click', () => {
            const id = Number(button.dataset.id);
            excluir_lembrete(id);
            mostrar_pagina_inicial();
        });
    });
}

function configurar_pagina_criar() {
    const form_criar = document.getElementById('form_criar');
    if (!form_criar) return;

    form_criar.addEventListener('submit', event => {
        event.preventDefault();
        const titulo = document.getElementById('titulo').value;
        const detalhes = document.getElementById('detalhes').value;
        criar_lembrete(titulo, detalhes);
        // Redirecionar para inicial mantendo o nome do usuário
        const nome = pegar_nome_usuario();
        window.location.href = nome ? `/inicial?nome=${encodeURIComponent(nome)}` : '/inicial';
    });
}

function deslogar() {
    localStorage.removeItem('nome_usuario');
}

