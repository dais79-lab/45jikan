import re
import json

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract existing courseData
match = re.search(r'const courseData = (\{[\s\S]*?\});', content)
if match:
    course_data = match.group(0)
else:
    print("Could not find courseData. Aborting.")
    exit()

# CSS Enhancements for RPG + Navigation
css_additions = """
        /* --- RPG & Nav Enhancements --- */
        .sidebar-item {
            padding: 15px;
            margin: 5px 0;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 700;
            color: #777;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: background 0.2s;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 1px;
        }

        .sidebar-item:hover {
            background: #f0f0f0;
        }

        .sidebar-item.active {
            background: #ddf4ff;
            color: var(--duo-blue);
            border: 2px solid var(--duo-blue-shadow);
        }

        .view-section {
            display: none;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }

        .view-section.active {
            display: block;
        }

        /* Avatar */
        .avatar-container {
            text-align: center;
            margin-bottom: 20px;
            padding: 20px;
            background: #fff;
            border-radius: 20px;
            border: 2px solid var(--card-border);
        }

        .avatar-img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: #eee;
            margin-bottom: 10px;
            object-fit: cover;
            border: 4px solid var(--duo-blue);
        }

        .level-badge {
            background: var(--duo-blue);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9rem;
            display: inline-block;
            font-weight: bold;
        }

        /* Vocab Grid */
        .vocab-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
        }

        .vocab-card {
            background: white;
            border: 2px solid var(--card-border);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 0 var(--card-border);
        }
        
        .vocab-jp { font-size: 1.5rem; margin-bottom: 5px; color: var(--text-color); }
        .vocab-es { font-size: 0.9rem; color: #777; }

        /* Shop Items */
        .shop-item {
            display: flex;
            align-items: center;
            background: white;
            border: 2px solid var(--card-border);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 0 var(--card-border);
        }

        .shop-icon { font-size: 2.5rem; margin-right: 20px; }
        .shop-info { flex: 1; }
        .shop-title { font-weight: bold; font-size: 1.1rem; }
        .shop-desc { font-size: 0.9rem; color: #777; }
        
        .buy-btn {
            background: white;
            border: 2px solid var(--card-border);
            padding: 10px 20px;
            border-radius: 12px;
            font-weight: bold;
            color: var(--duo-blue);
            cursor: pointer;
            box-shadow: 0 4px 0 var(--card-border);
        }
        
        .buy-btn:active { transform: translateY(4px); box-shadow: none; }
        
        .buy-btn.can-afford {
            background: var(--duo-blue);
            color: white;
            border-color: var(--duo-blue-shadow);
            box-shadow: 0 4px 0 var(--duo-blue-shadow);
        }
"""

# HTML for Sidebar and Views
html_structure = """
    <header class="app-header">
        <div style="font-size: 1.5rem; color: var(--duo-green); font-weight: 800;">nihongo RPG</div>
        <div class="stats-container">
            <div class="stat-item">
                <span>🛡️</span> <span id="level-display">Nvl 1</span>
            </div>
            <div class="stat-item active">
                <span>💎</span> <span id="xp-display">0</span>
            </div>
            <div class="stat-item hearts">
                <span>❤️</span> <span id="heart-count">5</span>
            </div>
        </div>
    </header>

    <div class="main-container">
        <div class="sidebar">
            <div class="avatar-container">
                <div style="font-size: 4rem;">🥷</div>
                <div class="level-badge" id="sidebar-level">Nivel 1</div>
                <div style="margin-top: 5px; color: #777; font-size: 0.9rem;">Aprendiz</div>
            </div>
            
            <div class="sidebar-item active" onclick="switchView('home', this)">
                <span>🏠</span> INICIO
            </div>
            <div class="sidebar-item" onclick="switchView('vocab', this)">
                <span>📚</span> VOCABULARIO
            </div>
            <div class="sidebar-item" onclick="switchView('shop', this)">
                <span>🛒</span> TIENDA
            </div>
        </div>
        
        <div class="content-area">
            <!-- VIEW: HOME -->
            <div id="view-home" class="view-section active">
                <div class="lesson-path" id="path-container">
                    <!-- Path generated by JS -->
                </div>
            </div>

            <!-- VIEW: VOCAB -->
            <div id="view-vocab" class="view-section">
                <h2 style="margin-bottom: 20px; color: var(--text-color);">Tu Colección de Palabras</h2>
                <div class="vocab-grid" id="vocab-container">
                    <p style="color: #777;">Completa lecciones para desbloquear palabras.</p>
                </div>
            </div>

            <!-- VIEW: SHOP -->
            <div id="view-shop" class="view-section">
                <h2 style="margin-bottom: 20px; color: var(--text-color);">Tienda de Objetos</h2>
                
                <div class="shop-item">
                    <div class="shop-icon">❤️</div>
                    <div class="shop-info">
                        <div class="shop-title">Rellenar Vidas</div>
                        <div class="shop-desc">Recupera todos tus corazones</div>
                    </div>
                    <button class="buy-btn can-afford" onclick="buyItem('refill_hearts', 50)">
                        💎 50
                    </button>
                </div>

                <div class="shop-item">
                    <div class="shop-icon">🛡️</div>
                    <div class="shop-info">
                        <div class="shop-title">Protector de Racha</div>
                        <div class="shop-desc">Protege tu racha por un día</div>
                    </div>
                    <button class="buy-btn" onclick="buyItem('streak_freeze', 200)">
                        💎 200
                    </button>
                </div>

                 <div class="shop-item">
                    <div class="shop-icon">👘</div>
                    <div class="shop-info">
                        <div class="shop-title">Traje de Samurai</div>
                        <div class="shop-desc">Avatar exclusivo</div>
                    </div>
                    <button class="buy-btn" onclick="buyItem('skin_samurai', 1000)">
                        💎 1000
                    </button>
                </div>
            </div>
        </div>
    </div>
"""

# JS Logic for Views & Shop
js_logic = """
    // --- State ---
    let gameState = {
        currentLessonId: null,
        currentQueue: [],
        currentIndex: 0,
        hearts: 5,
        streak: 0,
        completedLessons: [],
        xp: 100, // Currency
        level: 1,
        unlockedVocab: [] // Array of words
    };

    // --- Init ---
    document.addEventListener('DOMContentLoaded', () => {
        loadProgress();
        renderPath();
        updateStats();
        renderVocab();
    });

    function loadProgress() {
        const saved = localStorage.getItem('duo_rpg_state');
        if (saved) {
            const parsed = JSON.parse(saved);
            gameState = { ...gameState, ...parsed };
        }
    }

    function saveProgress() {
        localStorage.setItem('duo_rpg_state', JSON.stringify(gameState));
    }

    function updateStats() {
        document.getElementById('level-display').textContent = `Nvl ${gameState.level}`;
        document.getElementById('sidebar-level').textContent = `Nivel ${gameState.level}`;
        document.getElementById('xp-display').textContent = gameState.xp;
        document.getElementById('heart-count').textContent = gameState.hearts;
        document.getElementById('game-hearts').textContent = gameState.hearts;
        
        // Update shop buttons
        document.querySelectorAll('.buy-btn').forEach(btn => {
            const cost = parseInt(btn.innerText.replace('💎', '').trim());
            if (gameState.xp >= cost) btn.classList.add('can-afford');
            else btn.classList.remove('can-afford');
        });
    }

    // --- Navigation ---
    window.switchView = function(viewName, btnEl) {
        // Update Sidebar
        document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
        if(btnEl) btnEl.classList.add('active');

        // Update Views
        document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
        document.getElementById(`view-${viewName}`).classList.add('active');
        
        if (viewName === 'vocab') renderVocab();
    }

    // --- Vocab Render ---
    function renderVocab() {
        const container = document.getElementById('vocab-container');
        if (gameState.completedLessons.length === 0) {
            container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #999; padding: 40px;">Completa lecciones para desbloquear palabras en tu grimorio.</div>';
            return;
        }

        container.innerHTML = '';
        
        // Collect vocab from completed lessons
        let words = [];
        gameState.completedLessons.forEach(lid => {
            const lesson = courseData.lessons.find(l => l.id === lid);
            if (lesson && lesson.vocabulary) {
                words = [...words, ...lesson.vocabulary];
            }
        });
        
        // Remove duplicates and placeholders
        words = words.filter((v, i, a) => a.findIndex(t => t.kanji === v.kanji) === i && v.kanji !== '（こたえ）');

        words.forEach(word => {
            const card = document.createElement('div');
            card.className = 'vocab-card';
            card.innerHTML = `
                <div class="vocab-jp">${word.kanji}</div>
                <div class="vocab-es">${word.es}</div>
            `;
            container.appendChild(card);
        });
    }

    // --- Shop Logic ---
    window.buyItem = function(itemId, cost) {
        if (gameState.xp >= cost) {
            if (itemId === 'refill_hearts') {
                if (gameState.hearts >= 5) {
                    alert("¡Ya tienes la salud al máximo!");
                    return;
                }
                gameState.hearts = 5;
            } else {
                alert("¡Objeto comprado! (Efecto cosmético por ahora)");
            }
            
            gameState.xp -= cost;
            updateStats();
            saveProgress();
            // Play sound
        } else {
            alert("No tienes suficientes gemas (XP). ¡Completa más lecciones!");
        }
    }

    // --- Lesson Completion Hook ---
    // Update finishLesson to award XP and unlock vocab
    function finishLesson() {
        const rewardXP = 50;
        gameState.xp += rewardXP;
        
        // Level Up Logic (Simple: every 100 XP is a level, sort of)
        // Better: linear progression
        const newLevel = Math.floor(gameState.xp / 500) + 1;
        if (newLevel > gameState.level) {
            gameState.level = newLevel;
            alert(`¡SUBIDA DE NIVEL! Ahora eres Nivel ${gameState.level}`);
        }

        if (!gameState.completedLessons.includes(gameState.currentLessonId)) {
            gameState.completedLessons.push(gameState.currentLessonId);
        }
        
        gameState.streak++;
        saveProgress();
        updateStats();
        
        document.getElementById('game-overlay').classList.remove('active');
        document.getElementById('completion-screen').style.display = 'flex';
        // Update completion screen text
        document.querySelector('#completion-screen h2').textContent = "¡Misión Cumplida!";
        document.querySelector('#completion-screen .xp-reward').textContent = `+${rewardXP}`;
        
        renderPath();
    }
    
    // Helper to find finishLesson in existing code and replace or we overwrite it
    // Since we are rewriting the whole script block in python, we define it here.
"""

# Combine everything
full_html = content

# Inject CSS
full_html = full_html.replace('</style>', css_additions + '\n</style>')

# Replace Body content (Header + Main Container)
# We find the range from <header> to start of <script> (or end of main container)
# Actually, the previous file had a specific structure.
# Let's replace everything inside <body> until <script>
# Pattern: <body>(.*?)<script>
full_html = re.sub(r'<body>([\s\S]*?)<script>', f'<body>{html_structure}<script>', full_html)

# Replace JS Logic
# We need to preserve courseData but replace the rest of the logic
# Pattern: const courseData = {...}; (.*?) </script>
# We will construct the new script block manually.

script_content = f"""
    {course_data}

    {js_logic}

    // --- Path Render (Re-used) ---
    function renderPath() {{
        const container = document.getElementById('path-container');
        container.innerHTML = '';
        let unitCount = 1;
        
        courseData.lessons.forEach((lesson, index) => {{
            if (index % 4 === 0) {{
                const header = document.createElement('div');
                header.className = 'unit-header';
                header.innerHTML = `<h3>Unidad ${{unitCount}}</h3><p>Misiones de Rango F</p>`;
                container.appendChild(header);
                unitCount++;
            }}

            const isLocked = index > 0 && !gameState.completedLessons.includes(courseData.lessons[index-1].id) && !gameState.completedLessons.includes(lesson.id);
            const reallyLocked = (index === 0) ? false : isLocked;
            const offset = Math.sin(index) * 50; 

            const node = document.createElement('div');
            node.className = `lesson-node ${{reallyLocked ? 'locked' : ''}}`;
            node.style.transform = `translateX(${{offset}}px)`;
            
            const icon = gameState.completedLessons.includes(lesson.id) ? '⚔️' : (reallyLocked ? '🔒' : '🗡️');
            
            node.innerHTML = `
                <div style="font-size: 2rem;">${{icon}}</div>
                <div class="lesson-title">${{lesson.title}}</div>
            `;
            
            if (!reallyLocked) {{
                node.onclick = () => startLesson(lesson.id);
            }}

            container.appendChild(node);
        }});
    }}

    // --- Game Logic (Re-used & Adapted) ---
    function startLesson(id) {{
        gameState.currentLessonId = id;
        const lesson = courseData.lessons.find(l => l.id === id);
        let queue = [];
        
        // Vocab
        lesson.vocabulary.forEach(v => {{
            if (v.kanji === '（こたえ）') return;
            queue.push({{
                type: 'vocab_mc',
                prompt: `¿Qué significa "${{v.kanji}}"?`,
                correct: v.es,
                options: [v.es, "Opción Incorrecta 1", "Opción Incorrecta 2", "Opción Incorrecta 3"], 
                audio: v.audioText
            }});
        }});

        // Exercises
        if (lesson.exercises) {{
            lesson.exercises.forEach(ex => {{
                queue.push({{
                    type: 'exercise',
                    prompt: ex.question,
                    correct: ex.options.find(o => o.correct).text,
                    options: ex.options.map(o => o.text),
                    audio: null
                }});
            }});
        }}
        
        queue = queue.sort(() => 0.5 - Math.random());
        gameState.currentQueue = queue.slice(0, 10);
        gameState.currentIndex = 0;
        
        if (gameState.hearts <= 0) {{
            alert("¡Estás herido! Visita la tienda para curarte.");
            return;
        }}

        document.getElementById('game-overlay').classList.add('active');
        renderQuestion();
    }}

    let selectedOption = null;
    let currentQuestion = null;

    function renderQuestion() {{
        if (gameState.currentIndex >= gameState.currentQueue.length) {{
            finishLesson();
            return;
        }}

        currentQuestion = gameState.currentQueue[gameState.currentIndex];
        const body = document.getElementById('game-body');
        const progress = (gameState.currentIndex / gameState.currentQueue.length) * 100;
        document.getElementById('game-progress').style.width = `${{progress}}%`;
        
        document.getElementById('check-btn').disabled = true;
        document.getElementById('feedback-sheet').classList.remove('correct', 'wrong');
        document.getElementById('feedback-sheet').style.transform = 'translateY(100%)';
        selectedOption = null;

        let html = `<div class="question-text">${{currentQuestion.prompt}}</div>`;
        
        let opts = [...new Set(currentQuestion.options)];
        while(opts.length < 3) opts.push("Opción Extra");
        opts = opts.sort(() => 0.5 - Math.random());

        html += `<div class="options-grid">`;
        opts.forEach(opt => {{
            html += `<div class="option-card" onclick="selectOption(this, '${{opt.replace(/'/g, "\\\\'")}}')">${{opt}}</div>`;
        }});
        html += `</div>`;

        body.innerHTML = html;
    }}

    window.selectOption = function(el, text) {{
        document.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
        el.classList.add('selected');
        selectedOption = text;
        document.getElementById('check-btn').disabled = false;
    }}

    window.checkAnswer = function() {{
        const isCorrect = (selectedOption === currentQuestion.correct);
        const feedback = document.getElementById('feedback-sheet');
        const feedbackText = document.getElementById('feedback-text');
        
        document.querySelectorAll('.option-card').forEach(c => {{
            if (c.textContent === currentQuestion.correct) c.classList.add('correct');
            else if (c.classList.contains('selected') && !isCorrect) c.classList.add('wrong');
        }});

        if (isCorrect) {{
            feedback.className = 'feedback-sheet correct';
            feedbackText.textContent = "¡Golpe Crítico!";
        }} else {{
            feedback.className = 'feedback-sheet wrong';
            feedbackText.textContent = `Fallaste. Era: ${{currentQuestion.correct}}`;
            gameState.hearts--;
            updateStats();
            saveProgress();
            if (gameState.hearts <= 0) {{
                alert("¡Has sido derrotado! (Sin vidas)");
                closeGame();
                return;
            }}
        }}
    }}

    window.nextQuestion = function() {{
        gameState.currentIndex++;
        renderQuestion();
    }}

    window.closeCompletion = function() {{
        document.getElementById('completion-screen').style.display = 'none';
    }}

    window.closeGame = function() {{
        if (confirm("¿Huir de la batalla? Perderás el progreso.")) {{
            document.getElementById('game-overlay').classList.remove('active');
        }}
    }}
"""

# Replace the old script block entirely with the new one
full_html = re.sub(r'<script>[\s\S]*?</script>', f'<script>{script_content}</script>', full_html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("RPG + Duolingo merge complete!")
