import re
import json

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract courseData (we must preserve this!)
match = re.search(r'const courseData = (\{[\s\S]*?\});', content)
if not match:
    print("Error: Could not find courseData")
    exit()

course_data_js = match.group(0)

# New Duo-style HTML Structure and CSS
new_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nihongo Quest - Aprende Japonés</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --duo-green: #58cc02;
            --duo-green-shadow: #58a700;
            --duo-red: #ff4b4b;
            --duo-red-shadow: #d42020;
            --duo-blue: #1cb0f6;
            --duo-blue-shadow: #1899d6;
            --duo-yellow: #ffc800;
            --duo-yellow-shadow: #e5a500;
            --gray-bg: #f7f7f7;
            --card-border: #e5e5e5;
            --text-color: #3c3c3c;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Fredoka', sans-serif;
            background-color: white;
            color: var(--text-color);
            height: 100vh;
            overflow: hidden; /* App-like feel */
        }

        /* --- Header --- */
        .app-header {
            height: 60px;
            border-bottom: 2px solid var(--card-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            background: white;
            z-index: 100;
        }

        .stats-container {
            display: flex;
            gap: 20px;
        }

        .stat-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-weight: 700;
            color: #afafaf;
        }
        
        .stat-item.active { color: var(--duo-yellow); }
        .stat-item.hearts { color: var(--duo-red); }

        /* --- Layout --- */
        .main-container {
            display: flex;
            height: calc(100vh - 60px);
        }

        .sidebar {
            width: 250px;
            border-right: 2px solid var(--card-border);
            padding: 20px;
            display: none; /* Hidden on mobile */
        }
        
        @media (min-width: 768px) {
            .sidebar { display: block; }
        }

        .content-area {
            flex: 1;
            overflow-y: auto;
            position: relative;
            background-image: radial-gradient(#e5e5e5 1px, transparent 1px);
            background-size: 20px 20px;
        }

        /* --- Lesson Path --- */
        .lesson-path {
            padding: 40px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
            max-width: 400px;
            margin: 0 auto;
        }

        .unit-header {
            background: var(--duo-green);
            color: white;
            width: 100%;
            padding: 15px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 0 var(--duo-green-shadow);
        }

        .lesson-node {
            width: 70px;
            height: 70px;
            background: var(--duo-green);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 6px 0 var(--duo-green-shadow);
            cursor: pointer;
            position: relative;
            transition: transform 0.1s;
            margin: 10px;
        }

        .lesson-node:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0 var(--duo-green-shadow);
        }

        .lesson-node.locked {
            background: #e5e5e5;
            box-shadow: 0 6px 0 #cfcfcf;
            cursor: not-allowed;
            pointer-events: none;
        }

        .lesson-node img {
            width: 35px;
            height: 35px;
            filter: brightness(0) invert(1);
        }
        
        .lesson-node.locked img {
            filter: opacity(0.5);
        }

        .lesson-title {
            position: absolute;
            top: 80px;
            background: white;
            padding: 5px 10px;
            border-radius: 10px;
            border: 2px solid var(--card-border);
            font-size: 0.8rem;
            white-space: nowrap;
            display: none;
            z-index: 10;
        }
        
        .lesson-node:hover .lesson-title {
            display: block;
        }

        /* --- Game Overlay (Lesson Mode) --- */
        .game-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: white;
            z-index: 2000;
            display: none;
            flex-direction: column;
        }
        
        .game-overlay.active { display: flex; }

        .game-header {
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .close-btn {
            font-size: 1.5rem;
            cursor: pointer;
            color: #e5e5e5;
        }

        .progress-bar-container {
            flex: 1;
            height: 16px;
            background: #e5e5e5;
            border-radius: 8px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: var(--duo-green);
            width: 0%;
            transition: width 0.3s;
            border-radius: 8px;
        }

        .game-body {
            flex: 1;
            padding: 20px;
            max-width: 600px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .question-text {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            text-align: center;
        }

        .options-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        @media (max-width: 600px) {
            .options-grid { grid-template-columns: 1fr; }
        }

        .option-card {
            border: 2px solid var(--card-border);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.1s;
            box-shadow: 0 4px 0 var(--card-border);
        }

        .option-card:active {
            transform: translateY(4px);
            box-shadow: none;
        }

        .option-card.selected {
            border-color: var(--duo-blue);
            background: #ddf4ff;
            color: var(--duo-blue);
            box-shadow: 0 4px 0 var(--duo-blue-shadow);
        }

        .option-card.correct {
            border-color: var(--duo-green);
            background: #d7ffb8;
            color: var(--duo-green);
        }
        
        .option-card.wrong {
            border-color: var(--duo-red);
            background: #ffdfe0;
            color: var(--duo-red);
        }

        .game-footer {
            padding: 20px;
            border-top: 2px solid var(--card-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .check-btn {
            background: var(--duo-green);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 15px;
            font-weight: 700;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 0 var(--duo-green-shadow);
            cursor: pointer;
            width: 100%;
            max-width: 200px;
            margin-left: auto;
        }
        
        .check-btn:disabled {
            background: #e5e5e5;
            color: #afafaf;
            box-shadow: none;
            cursor: default;
        }

        /* --- Bottom Sheet Feedback --- */
        .feedback-sheet {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 20px;
            transform: translateY(100%);
            transition: transform 0.3s;
            z-index: 2001;
        }

        .feedback-sheet.correct {
            background: #d7ffb8;
            color: var(--duo-green);
            transform: translateY(0);
        }

        .feedback-sheet.wrong {
            background: #ffdfe0;
            color: var(--duo-red);
            transform: translateY(0);
        }

        .feedback-content {
            max-width: 600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .next-btn {
            background: white; /* Will be colored by context */
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            border: 2px solid rgba(0,0,0,0.1);
        }

    </style>
</head>
<body>

    <header class="app-header">
        <div style="font-size: 1.5rem; color: var(--duo-green); font-weight: 800;">nihongo</div>
        <div class="stats-container">
            <div class="stat-item active">
                <span>🔥</span> <span id="streak-count">0</span>
            </div>
            <div class="stat-item hearts">
                <span>❤️</span> <span id="heart-count">5</span>
            </div>
        </div>
    </header>

    <div class="main-container">
        <div class="sidebar">
            <h3>Menú</h3>
            <p style="margin-top: 10px; color: #777;">Inicio</p>
            <p style="margin-top: 10px; color: #777;">Vocabulario</p>
            <p style="margin-top: 10px; color: #777;">Tienda</p>
        </div>
        <div class="content-area">
            <div class="lesson-path" id="path-container">
                <!-- Path generated by JS -->
            </div>
        </div>
    </div>

    <!-- Game Overlay -->
    <div class="game-overlay" id="game-overlay">
        <div class="game-header">
            <div class="close-btn" onclick="closeGame()">✕</div>
            <div class="progress-bar-container">
                <div class="progress-fill" id="game-progress"></div>
            </div>
            <div class="stat-item hearts">
                <span>❤️</span> <span id="game-hearts">5</span>
            </div>
        </div>
        
        <div class="game-body" id="game-body">
            <!-- Dynamic Question Content -->
        </div>

        <div class="game-footer">
            <div id="footer-msg"></div>
            <button class="check-btn" id="check-btn" onclick="checkAnswer()" disabled>COMPROBAR</button>
        </div>

        <div class="feedback-sheet" id="feedback-sheet">
            <div class="feedback-content">
                <div id="feedback-text" style="font-size: 1.5rem; font-weight: bold;"></div>
                <button class="check-btn" onclick="nextQuestion()" style="margin: 0; background: white; color: inherit; border: 2px solid rgba(0,0,0,0.1);">CONTINUAR</button>
            </div>
        </div>
    </div>

    <!-- Completion Modal -->
    <div class="game-overlay" id="completion-screen" style="z-index: 2005; background: var(--duo-yellow); align-items: center; justify-content: center; text-align: center;">
        <div style="background: white; padding: 40px; border-radius: 20px; max-width: 400px; width: 90%;">
            <div style="font-size: 5rem;">🎉</div>
            <h2 style="color: var(--duo-yellow-shadow); margin: 20px 0;">¡Lección Completada!</h2>
            <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;">
                <div style="text-align: center;">
                    <div style="font-weight: bold; color: var(--duo-yellow);">XP GANADA</div>
                    <div style="font-size: 2rem; font-weight: 800;">+20</div>
                </div>
            </div>
            <button class="check-btn" onclick="closeCompletion()" style="width: 100%;">CONTINUAR</button>
        </div>
    </div>

    <script>
    // --- Data ---
    COURSE_DATA_PLACEHOLDER

    // --- State ---
    let gameState = {
        currentLessonId: null,
        currentQueue: [], // Array of question objects
        currentIndex: 0,
        hearts: 5,
        streak: 0,
        completedLessons: [], // IDs
        xp: 0
    };

    // --- Init ---
    document.addEventListener('DOMContentLoaded', () => {
        loadProgress();
        renderPath();
        updateStats();
    });

    function loadProgress() {
        const saved = localStorage.getItem('duo_state');
        if (saved) {
            const parsed = JSON.parse(saved);
            gameState.hearts = parsed.hearts || 5;
            gameState.streak = parsed.streak || 0;
            gameState.completedLessons = parsed.completedLessons || [];
            gameState.xp = parsed.xp || 0;
        }
    }

    function saveProgress() {
        localStorage.setItem('duo_state', JSON.stringify(gameState));
    }

    function updateStats() {
        document.getElementById('streak-count').textContent = gameState.streak;
        document.getElementById('heart-count').textContent = gameState.hearts;
        document.getElementById('game-hearts').textContent = gameState.hearts;
    }

    // --- Path Render ---
    function renderPath() {
        const container = document.getElementById('path-container');
        container.innerHTML = '';

        // Group by 3 for visual spacing maybe, or just linear
        // Let's create unit headers for every 3 lessons
        
        let unitCount = 1;
        
        courseData.lessons.forEach((lesson, index) => {
            if (index % 4 === 0) {
                const header = document.createElement('div');
                header.className = 'unit-header';
                header.innerHTML = `<h3>Unidad ${unitCount}</h3><p>Conceptos básicos</p>`;
                container.appendChild(header);
                unitCount++;
            }

            const isLocked = index > 0 && !gameState.completedLessons.includes(courseData.lessons[index-1].id) && !gameState.completedLessons.includes(lesson.id);
            // First lesson is always unlocked
            const reallyLocked = (index === 0) ? false : isLocked;
            
            // Random horizontal offset for "winding path" look
            const offset = Math.sin(index) * 50; 

            const node = document.createElement('div');
            node.className = `lesson-node ${reallyLocked ? 'locked' : ''}`;
            node.style.transform = `translateX(${offset}px)`;
            
            // Star icon or Book icon
            const icon = gameState.completedLessons.includes(lesson.id) ? '⭐' : '📖';
            
            node.innerHTML = `
                <div style="font-size: 2rem;">${icon}</div>
                <div class="lesson-title">${lesson.title}</div>
            `;
            
            if (!reallyLocked) {
                node.onclick = () => startLesson(lesson.id);
            }

            container.appendChild(node);
        });
    }

    // --- Game Logic ---
    function startLesson(id) {
        gameState.currentLessonId = id;
        const lesson = courseData.lessons.find(l => l.id === id);
        
        // Build Queue: Vocab -> Phrases -> Exercises
        // We'll mix them or do sequential.
        // Let's create 5-10 questions.
        
        let queue = [];
        
        // 1. Vocab flashcards (transformed to multiple choice)
        lesson.vocabulary.forEach(v => {
            if (v.kanji === '（こたえ）') return;
            queue.push({
                type: 'vocab_mc',
                prompt: `¿Qué significa "${v.kanji}"?`,
                correct: v.es,
                options: [v.es, "Opción Incorrecta 1", "Opción Incorrecta 2", "Opción Incorrecta 3"], // We need real distractors
                audio: v.audioText
            });
        });

        // 2. Exercises from data
        if (lesson.exercises) {
            lesson.exercises.forEach(ex => {
                queue.push({
                    type: 'exercise',
                    prompt: ex.question,
                    correct: ex.options.find(o => o.correct).text,
                    options: ex.options.map(o => o.text),
                    audio: null
                });
            });
        }
        
        // Shuffle queue
        queue = queue.sort(() => 0.5 - Math.random());
        // Limit to 10
        gameState.currentQueue = queue.slice(0, 10);
        gameState.currentIndex = 0;
        
        // Reset Hearts for lesson? No, global hearts.
        if (gameState.hearts <= 0) {
            alert("¡No tienes vidas! Espera o practica para recuperar.");
            gameState.hearts = 5; // Cheat for demo
            saveProgress();
            updateStats();
        }

        document.getElementById('game-overlay').classList.add('active');
        renderQuestion();
    }

    let selectedOption = null;
    let currentQuestion = null;

    function renderQuestion() {
        if (gameState.currentIndex >= gameState.currentQueue.length) {
            finishLesson();
            return;
        }

        currentQuestion = gameState.currentQueue[gameState.currentIndex];
        const body = document.getElementById('game-body');
        const progress = (gameState.currentIndex / gameState.currentQueue.length) * 100;
        document.getElementById('game-progress').style.width = `${progress}%`;
        
        // Reset UI
        document.getElementById('check-btn').disabled = true;
        document.getElementById('feedback-sheet').classList.remove('correct', 'wrong');
        document.getElementById('feedback-sheet').style.transform = 'translateY(100%)';
        selectedOption = null;

        // Render
        let html = `<div class="question-text">${currentQuestion.prompt}</div>`;
        
        // Options
        // Ensure options are unique and shuffled
        let opts = [...new Set(currentQuestion.options)];
        // Fill with dummy if needed (simple logic)
        while(opts.length < 3) opts.push("Opción Extra");
        opts = opts.sort(() => 0.5 - Math.random());

        html += `<div class="options-grid">`;
        opts.forEach(opt => {
            html += `<div class="option-card" onclick="selectOption(this, '${opt.replace(/'/g, "\\'")}')">${opt}</div>`;
        });
        html += `</div>`;

        body.innerHTML = html;
    }

    window.selectOption = function(el, text) {
        // Deselect others
        document.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
        el.classList.add('selected');
        selectedOption = text;
        document.getElementById('check-btn').disabled = false;
        
        // Play click sound (optional)
    }

    window.checkAnswer = function() {
        const isCorrect = (selectedOption === currentQuestion.correct);
        const feedback = document.getElementById('feedback-sheet');
        const feedbackText = document.getElementById('feedback-text');
        
        document.querySelectorAll('.option-card').forEach(c => {
            if (c.textContent === currentQuestion.correct) c.classList.add('correct');
            else if (c.classList.contains('selected') && !isCorrect) c.classList.add('wrong');
        });

        if (isCorrect) {
            feedback.className = 'feedback-sheet correct';
            feedbackText.textContent = "¡Increíble!";
            // Play success sound
        } else {
            feedback.className = 'feedback-sheet wrong';
            feedbackText.textContent = `Correcto: ${currentQuestion.correct}`;
            gameState.hearts--;
            updateStats();
            saveProgress();
            if (gameState.hearts <= 0) {
                alert("¡Oh no! Te has quedado sin vidas.");
                closeGame();
                return;
            }
        }
        
        // Hide check button, show sheet
        // document.getElementById('check-btn').style.display = 'none'; // Actually sheet covers it
    }

    window.nextQuestion = function() {
        gameState.currentIndex++;
        renderQuestion();
    }

    function finishLesson() {
        gameState.xp += 20;
        if (!gameState.completedLessons.includes(gameState.currentLessonId)) {
            gameState.completedLessons.push(gameState.currentLessonId);
        }
        gameState.streak++; // Simple streak logic
        saveProgress();
        
        document.getElementById('game-overlay').classList.remove('active');
        document.getElementById('completion-screen').style.display = 'flex';
        renderPath();
    }

    window.closeCompletion = function() {
        document.getElementById('completion-screen').style.display = 'none';
    }

    window.closeGame = function() {
        if (confirm("¿Salir? Perderás el progreso de esta lección.")) {
            document.getElementById('game-overlay').classList.remove('active');
        }
    }

    </script>
</body>
</html>"""

# Inject courseData
final_content = new_html.replace('COURSE_DATA_PLACEHOLDER', course_data_js)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Duolingo transformation complete!")
