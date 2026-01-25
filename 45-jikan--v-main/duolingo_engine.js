document.addEventListener('DOMContentLoaded', () => {
    initDuolingoApp();
});

let lives = 3;
window.getLives = () => lives; // Expose lives for 3D mode
let hintTimer = null;
const HINT_DELAY = 10000; // 10 seconds

function initDuolingoApp() {
    // 1. Scrape Data
    const data = scrapeLessonData();
    
    // --- Message passing for 3D Mode (File Protocol Support) ---
    if (window.parent && window.parent !== window) {
        console.log("Sending lesson data to parent (3D mode support)");
        window.parent.postMessage({ type: 'DUOLINGO_DATA', data: data }, '*');
    }
    // -----------------------------------------------------------

    if (!data.vocab.length && !data.quiz.length) {
        console.log("No lesson data found, staying in default mode.");
        return;
    }

    // 2. Hide Original Content
    const page = document.querySelector('.page');
    if (page) page.style.display = 'none';
    document.body.style.backgroundColor = '#fff';

    // 3. Create App Container
    const app = document.createElement('div');
    app.id = 'duo-app';
    document.body.appendChild(app);

    // 4. Start App
    runDuolingoFlow(data, app);
}

function scrapeLessonData() {
    const data = { vocab: [], quiz: [] };
    
    // Vocab
    document.querySelectorAll('.vocab-grid tr').forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 3) {
            data.vocab.push({
                jp: cells[0].innerText.trim(),
                kana: cells[1].innerText.trim(),
                es: cells[2].innerText.trim()
            });
        }
    });

    // Quiz
    const answers = {};
    document.querySelectorAll('.ans-item').forEach(item => {
        const parts = item.innerText.split('.');
        if (parts.length >= 2) {
            answers[parts[0].trim()] = parts[1].trim();
        }
    });

    document.querySelectorAll('.quiz-item').forEach((item, index) => {
        const qNum = index + 1;
        const qElem = item.querySelector('.quiz-q');
        if (!qElem) return;
        
        const question = qElem.innerText.replace(/^\d+\.\s*/, '');
        const optionsText = item.querySelector('.quiz-options').innerText;
        const options = optionsText.split('/').map(opt => {
            const trimmed = opt.trim();
            const dotIdx = trimmed.indexOf('.');
            return {
                letter: trimmed.substring(0, dotIdx).trim(),
                text: trimmed.substring(dotIdx + 1).trim()
            };
        });

        data.quiz.push({
            id: qNum,
            question: question,
            options: options,
            correctLetter: answers[qNum]
        });
    });

    return data;
}

function runDuolingoFlow(data, container) {
    let currentStep = 0;
    const steps = [
        ...data.vocab.map(v => ({ type: 'vocab', data: v })),
        ...data.quiz.map(q => ({ type: 'quiz', data: q })),
        { type: 'finish' }
    ];

    function render() {
        // Clear existing hint timer
        if (hintTimer) clearTimeout(hintTimer);

        if (lives <= 0) {
            renderGameOver();
            return;
        }

        if (currentStep >= steps.length) return;
        const step = steps[currentStep];
        const progress = (currentStep / (steps.length - 1)) * 100;

        // Generate hearts HTML
        let heartsHtml = '';
        for (let i = 0; i < lives; i++) {
            heartsHtml += '<span class="heart-icon">❤️</span>';
        }

        // Header
        let html = `
            <div class="duo-header">
                <a href="../../index.html" class="close-btn">✕</a>
                <div class="progress-container">
                    <div class="progress-bar" style="width: ${progress}%"></div>
                </div>
                <div class="hearts-container" id="hearts-display">
                    ${heartsHtml}
                </div>
            </div>
            <div class="duo-content">
        `;

        if (step.type === 'vocab') {
            html += `
                <div class="character-area duck-idle">🦆</div>
                <div class="vocab-card">
                    <div class="audio-circle" onclick="speak('${step.data.jp}')">🔊</div>
                    <div class="jp-word">${step.data.jp}</div>
                    <div class="kana-word">${step.data.kana}</div>
                    <div class="es-word">${step.data.es}</div>
                </div>
                <button class="check-btn" onclick="nextStep()">Entendido</button>
            `;
        } else if (step.type === 'quiz') {
            html += `
                <div class="character-area duck-idle">
                    🦆
                    <div class="hint-bubble" id="hint-bubble">¡Pst! Intenta con "${step.data.correctLetter}"...</div>
                </div>
                <div class="quiz-question">${step.data.question}</div>
                <div class="options-grid">
                    ${step.data.options.map(opt => `
                        <div class="option-btn" onclick="selectOption(this, '${opt.letter}', '${step.data.correctLetter}')">
                            ${opt.text}
                        </div>
                    `).join('')}
                </div>
                <div id="feedback-area"></div>
            `;
            
            // Start hint timer for quiz
            hintTimer = setTimeout(() => {
                const bubble = document.getElementById('hint-bubble');
                if (bubble) bubble.classList.add('show');
            }, HINT_DELAY);
        } else if (step.type === 'finish') {
             // Save Progress
             try {
                // Save both filename-based key and src-based key if possible
                const filename = window.location.pathname.split('/').pop();
                const lessonKey = 'progress_' + filename;
                localStorage.setItem(lessonKey, 'true');
                console.log("Saved progress:", lessonKey);
                
                // Also try to save the path relative to root for index.html compatibility
                // We assume structure starts with "45 jikan para subir"
                const decodedPath = decodeURIComponent(window.location.pathname);
                const index = decodedPath.indexOf("45 jikan para subir");
                if (index !== -1) {
                    const relativePath = decodedPath.substring(index);
                    const key2 = 'progress_' + relativePath;
                    localStorage.setItem(key2, 'true');
                    console.log("Saved root progress:", key2);
                }
            } catch (e) { console.error(e); }

            html += `
                <div class="character-area duck-success">🎉</div>
                <h1 style="color:#58cc02; font-size: 3rem;">¡Lección Completada!</h1>
                <p style="font-size: 1.5rem; color: #777;">Has aprendido nuevas palabras.</p>
                <button class="check-btn" onclick="window.location.href='../../index.html'">Volver al Menú</button>
            `;
        }

        html += `</div>`;
        container.innerHTML = html;
        
        if (step.type === 'vocab') {
            setTimeout(() => speak(step.data.jp), 300);
        }
    }

    function renderGameOver() {
        const container = document.querySelector('.duo-content');
        // Clear header
        document.querySelector('.duo-header').innerHTML = `
            <a href="../../index.html" class="close-btn" style="color:#4b4b4b">✕</a>
        `;
        
        container.innerHTML = `
            <div class="duck-dead-wrapper">
                <div style="font-size: 5rem;">🦆</div>
                <div class="duck-eyes-x">X X</div>
            </div>
            <h1 style="color:#ff4b4b; font-size: 3rem; margin-top: 20px;">¡Oh no!</h1>
            <p style="font-size: 1.5rem; color: #777;">Te has quedado sin vidas.</p>
            <button class="check-btn wrong" onclick="restartLesson()">Intentar de nuevo</button>
        `;
    }

    window.restartLesson = () => {
        lives = 3;
        currentStep = 0;
        render();
    };

    window.nextStep = () => {
        currentStep++;
        render();
    };

    window.selectOption = (btn, letter, correct) => {
        // Prevent multiple clicks
        if (btn.parentElement.classList.contains('answered')) return;
        btn.parentElement.classList.add('answered');
        
        // Stop hint timer
        if (hintTimer) clearTimeout(hintTimer);
        const bubble = document.getElementById('hint-bubble');
        if (bubble) bubble.classList.remove('show');

        if (letter === correct) {
            btn.classList.add('correct');
            playSound('correct');
            
            // Success Animation
            const charArea = document.querySelector('.character-area');
            charArea.classList.remove('duck-idle');
            void charArea.offsetWidth; // trigger reflow
            charArea.classList.add('duck-success');
            
            showFeedback(true);
        } else {
            btn.classList.add('wrong');
            playSound('wrong');
            
            // Lose Life
            lives--;
            updateHearts();
            
            const charArea = document.querySelector('.character-area');
            charArea.innerText = '🦆💧'; // Sad duck
            
            showFeedback(false, correct);
        }
    };

    function updateHearts() {
        const container = document.getElementById('hearts-display');
        if (!container) return;
        
        // Re-render hearts based on lives
        let html = '';
        for (let i = 0; i < Math.max(0, lives); i++) {
            html += '<span class="heart-icon">❤️</span>';
        }
        // Add broken hearts for animation? Simple re-render is fine for now
        // Or add a "lost" heart animation
        container.innerHTML = html + '<span class="heart-icon heart-lost">💔</span>';
    }

    function showFeedback(isCorrect, correctLetter) {
        const feedback = document.createElement('div');
        feedback.className = `feedback-overlay ${isCorrect ? 'correct' : 'wrong'}`;
        feedback.style.display = 'block';
        
        let btnAction = isCorrect ? 'nextStep()' : (lives > 0 ? 'nextStep()' : 'render()'); // If lives > 0 continue, else re-render triggers game over check

        feedback.innerHTML = `
            <div>${isCorrect ? '¡Correcto!' : 'Incorrecto...'}</div>
            <button class="check-btn ${isCorrect ? 'continue' : 'wrong'}" 
                style="margin-top:10px; background: white; color: ${isCorrect ? '#58cc02' : '#ea2b2b'}"
                onclick="${btnAction}">CONTINUAR</button>
        `;
        document.querySelector('.duo-content').appendChild(feedback);
    }

    render();
}

function speak(text) {
    window.speechSynthesis.cancel();
    const msg = new SpeechSynthesisUtterance(text);
    msg.lang = 'ja-JP';
    window.speechSynthesis.speak(msg);
}

function playSound(type) {
    const audio = new Audio(type === 'correct' ? '../../duolingo-correct.mp3' : '../../duolingo-wrong.mp3');
    audio.play().catch(e => console.log("Audio play failed", e));
}
