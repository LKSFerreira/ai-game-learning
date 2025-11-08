// --- CONFIGURAÇÃO ---
// Adicione o caminho para novos arquivos de quiz aqui para que apareçam no menu.
const ARQUIVOS_QUIZ = [
    'fase-1/perguntas_fase_1.json',
    'fase-2/perguntas_fase_2.json'
];
const NUM_QUESTOES_GERAL = 30;

// --- ELEMENTOS DO DOM ---
const telaSelecaoEl = document.getElementById('tela-selecao');
const botoesSelecaoEl = document.getElementById('botoes-selecao');
const quizContainerEl = document.getElementById('quiz-container');
const tituloQuizEl = document.getElementById('titulo-quiz');
const contadorPerguntaEl = document.getElementById('contador-pergunta');
const textoPerguntaEl = document.getElementById('texto-pergunta');
const botoesRespostaEl = document.getElementById('botoes-resposta');
const btnProximo = document.getElementById('btn-proximo');
const telaResultadoEl = document.getElementById('tela-resultado');
const textoResultadoEl = document.getElementById('texto-resultado');
const mensagemFinalEl = document.getElementById('mensagem-final');
const btnReiniciar = document.getElementById('btn-reiniciar');
const btnVoltarMenu = document.getElementById('btn-voltar-menu');

// --- LÓGICA DO CONFETE (sem alterações) ---
const confettiCanvas = document.getElementById('confetti-canvas');
const confettiCtx = confettiCanvas.getContext('2d');
let confettiParticles = [];
const confettiDefaults = { colors: ['#BB86FC', '#03DAC6', '#CF6679', '#FFE082', '#FFFFFF'], particleCount: 150, spread: 60, startVelocity: 45, decay: 0.9, gravity: 0.8 };
function resetCanvas() { confettiCanvas.width = window.innerWidth; confettiCanvas.height = window.innerHeight; }
function createConfetti() {
    resetCanvas();
    confettiParticles = [];
    for (let i = 0; i < confettiDefaults.particleCount; i++) { confettiParticles.push(createParticle(confettiCanvas.width / 2, confettiCanvas.height * 0.4)); }
    animateConfetti();
}
function createParticle(x, y) {
    const angle = Math.random() * confettiDefaults.spread * 2 - confettiDefaults.spread;
    const velocity = Math.random() * (confettiDefaults.startVelocity / 2) + (confettiDefaults.startVelocity / 2);
    return { x: x, y: y, color: confettiDefaults.colors[Math.floor(Math.random() * confettiDefaults.colors.length)], radius: Math.random() * 4 + 2, vx: Math.sin(angle * Math.PI / 180) * velocity, vy: -Math.cos(angle * Math.PI / 180) * velocity, alpha: 1 };
}
let animationFrameId;
function animateConfetti() {
    confettiCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
    confettiParticles.forEach((particle, index) => {
        particle.vy += confettiDefaults.gravity; particle.vx *= confettiDefaults.decay; particle.x += particle.vx; particle.y += particle.vy; particle.alpha -= 0.01;
        if (particle.alpha <= 0) { confettiParticles.splice(index, 1); } else { confettiCtx.globalAlpha = particle.alpha; confettiCtx.beginPath(); confettiCtx.fillStyle = particle.color; confettiCtx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2); confettiCtx.fill(); }
    });
    if (confettiParticles.length > 0) { animationFrameId = requestAnimationFrame(animateConfetti); } else { confettiCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height); }
}

// --- LÓGICA DO QUIZ ---
let todasAsPerguntas = {};
let perguntasAtuais = [];
let indexPerguntaAtual;
let pontuacao = 0;
let faseAtual = null;

async function carregarTodosOsQuizzes() {
    for (const arquivo of ARQUIVOS_QUIZ) {
        try {
            const response = await fetch(arquivo);
            if (!response.ok) throw new Error(`Falha ao carregar ${arquivo}`);
            const data = await response.json();
            todasAsPerguntas[data.fase] = data;
        } catch (error) {
            console.error(error);
        }
    }
}

function gerarMenuPrincipal() {
    botoesSelecaoEl.innerHTML = ''; // Limpa o menu
    for (const fase in todasAsPerguntas) {
        const quiz = todasAsPerguntas[fase];
        const button = document.createElement('button');
        button.innerText = quiz.titulo;
        button.classList.add('btn-selecao');
        button.dataset.fase = quiz.fase;
        button.addEventListener('click', () => iniciarQuiz(quiz.fase));
        botoesSelecaoEl.appendChild(button);
    }
    // Adicionar botão Geral
    if (Object.keys(todasAsPerguntas).length > 1) {
        const buttonGeral = document.createElement('button');
        buttonGeral.innerText = 'Quiz Geral (Aleatório)';
        buttonGeral.classList.add('btn-selecao', 'geral');
        buttonGeral.addEventListener('click', () => iniciarQuiz('geral'));
        botoesSelecaoEl.appendChild(buttonGeral);
    }
}

function iniciarQuiz(fase) {
    faseAtual = fase;
    pontuacao = 0;
    
    telaSelecaoEl.classList.add('hide');
    telaResultadoEl.classList.add('hide');
    mensagemFinalEl.classList.add('hide');
    quizContainerEl.classList.remove('hide');

    if (fase === 'geral') {
        let poolGeral = [];
        for (const key in todasAsPerguntas) {
            poolGeral.push(...todasAsPerguntas[key].perguntas);
        }
        perguntasAtuais = poolGeral.sort(() => Math.random() - 0.5).slice(0, NUM_QUESTOES_GERAL);
        tituloQuizEl.innerText = "Quiz Geral";
    } else {
        const quizData = todasAsPerguntas[fase];
        perguntasAtuais = [...quizData.perguntas].sort(() => Math.random() - 0.5);
        tituloQuizEl.innerText = quizData.titulo;
    }

    indexPerguntaAtual = 0;
    definirProximaPergunta();
}

function definirProximaPergunta() {
    resetarEstado();
    mostrarPergunta(perguntasAtuais[indexPerguntaAtual]);
}

function mostrarPergunta(pergunta) {
    contadorPerguntaEl.innerText = `Pergunta ${indexPerguntaAtual + 1} de ${perguntasAtuais.length}`;
    textoPerguntaEl.innerText = pergunta.pergunta;
    
    const respostasEmbaralhadas = pergunta.respostas.sort(() => Math.random() - 0.5);
    respostasEmbaralhadas.forEach(resposta => {
        const button = document.createElement('button');
        button.innerText = resposta.texto;
        button.classList.add('btn');
        button.dataset.correto = resposta.correto;
        button.addEventListener('click', selecionarResposta);
        botoesRespostaEl.appendChild(button);
    });
}

function resetarEstado() {
    btnProximo.classList.add('hide');
    while (botoesRespostaEl.firstChild) {
        botoesRespostaEl.removeChild(botoesRespostaEl.firstChild);
    }
}

function selecionarResposta(e) {
    const btnSelecionado = e.target;
    const correto = btnSelecionado.dataset.correto === "true";
    if (correto) {
        pontuacao++;
        createConfetti();
    }
    Array.from(botoesRespostaEl.children).forEach(button => {
        definirStatusClasse(button, button.dataset.correto === "true");
        button.disabled = true;
    });
    if (perguntasAtuais.length > indexPerguntaAtual + 1) {
        btnProximo.classList.remove('hide');
    } else {
        setTimeout(mostrarResultado, 1000);
    }
}

function mostrarResultado() {
    quizContainerEl.classList.add('hide');
    telaResultadoEl.classList.remove('hide');

    const total = perguntasAtuais.length;
    const porcentagem = total > 0 ? Math.round((pontuacao / total) * 100) : 0;
    textoResultadoEl.innerText = `Você acertou ${pontuacao} de ${total} perguntas (${porcentagem}%)!`;

    if (porcentagem >= 80) {
        mensagemFinalEl.innerText = "Parabéns!";
        mensagemFinalEl.classList.remove('hide');
        createConfetti();
    } else {
        mensagemFinalEl.classList.add('hide');
    }
}

function definirStatusClasse(elemento, correto) {
    elemento.classList.remove('correto', 'incorreto');
    if (correto) elemento.classList.add('correto');
    else elemento.classList.add('incorreto');
}

function mostrarMenu() {
    telaResultadoEl.classList.add('hide');
    quizContainerEl.classList.add('hide');
    telaSelecaoEl.classList.remove('hide');
}

// --- INICIALIZAÇÃO E EVENT LISTENERS ---
document.addEventListener('DOMContentLoaded', async () => {
    await carregarTodosOsQuizzes();
    gerarMenuPrincipal();
});

btnProximo.addEventListener('click', () => {
    indexPerguntaAtual++;
    definirProximaPergunta();
});

btnReiniciar.addEventListener('click', () => iniciarQuiz(faseAtual));
btnVoltarMenu.addEventListener('click', mostrarMenu);
window.addEventListener('resize', resetCanvas);