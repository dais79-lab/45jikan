import os
import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Google Font (Fredoka One or similar for gamey feel)
if "Fredoka One" not in content:
    content = content.replace(
        '<head>', 
        '<head>\n    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&display=swap" rel="stylesheet">'
    )

# 2. Update CSS
new_css = """
        /* Gameification Styles */
        :root {
            --level-bg: #4ecdc4;
            --xp-bg: #ffe66d;
            --xp-text: #555;
            --font-game: 'Fredoka', sans-serif;
        }

        body {
            font-family: var(--font-game);
        }

        .player-stats {
            background: rgba(0,0,0,0.2);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 1rem;
            margin-top: 1rem;
            backdrop-filter: blur(5px);
        }

        .level-badge {
            background: var(--level-bg);
            color: white;
            padding: 0.2rem 0.8rem;
            border-radius: 12px;
            font-weight: bold;
            box-shadow: 0 2px 0 rgba(0,0,0,0.2);
        }

        .xp-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: white;
            font-weight: bold;
        }

        .xp-bar-mini {
            width: 100px;
            height: 10px;
            background: rgba(255,255,255,0.3);
            border-radius: 5px;
            overflow: hidden;
        }

        .xp-fill-mini {
            height: 100%;
            background: var(--xp-bg);
            width: 0%;
            transition: width 0.5s ease;
        }

        /* Floating XP Animation */
        .floating-xp {
            position: fixed;
            color: var(--xp-bg);
            font-weight: bold;
            font-size: 1.5rem;
            pointer-events: none;
            animation: floatUp 1s ease-out forwards;
            z-index: 9999;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        @keyframes floatUp {
            0% { transform: translateY(0) scale(1); opacity: 1; }
            100% { transform: translateY(-50px) scale(1.5); opacity: 0; }
        }

        /* Level Up Modal */
        .level-up-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 3000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }

        .level-up-modal.active {
            opacity: 1;
            pointer-events: all;
        }

        .level-up-content {
            background: white;
            padding: 3rem;
            border-radius: 20px;
            text-align: center;
            transform: scale(0.8);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 5px solid var(--level-bg);
        }

        .level-up-modal.active .level-up-content {
            transform: scale(1);
        }

        .level-up-title {
            font-size: 3rem;
            color: var(--level-bg);
            margin-bottom: 1rem;
            text-shadow: 2px 2px 0 #eee;
        }

        /* Card flip animation 3D */
        .flashcard {
            transform-style: preserve-3d;
            transition: transform 0.6s;
        }
        
        .flashcard.flipped {
            transform: rotateY(180deg);
        }

        .card-front, .card-back {
            backface-visibility: hidden;
        }

        .card-back {
            transform: rotateY(180deg);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            background: white;
            border-radius: var(--border-radius);
        }
        
        /* Button Press Effect */
        .btn:active {
            transform: translateY(2px);
            box-shadow: none;
        }
"""

# Inject CSS
if "/* Gameification Styles */" not in content:
    content = content.replace('</style>', new_css + '\n    </style>')

# 3. Inject HTML for Header Stats
header_html = """
    <header>
        <h1>🇯🇵 Curso de Japonés RPG</h1>
        <div class="player-stats">
            <div class="level-badge">Nvl. <span id="player-level">1</span></div>
            <div class="xp-container">
                <span>XP</span>
                <div class="xp-bar-mini">
                    <div class="xp-fill-mini" id="xp-fill"></div>
                </div>
                <span id="xp-text">0 / 1000</span>
            </div>
        </div>
    </header>
"""
# Replace existing header
content = re.sub(r'<header>[\s\S]*?</header>', header_html, content)

# 4. Inject Level Up Modal HTML
modal_html = """
    <!-- Level Up Modal -->
    <div class="level-up-modal" id="level-up-modal">
        <div class="level-up-content">
            <div style="font-size: 5rem;">🎉</div>
            <h2 class="level-up-title">¡SUBIDA DE NIVEL!</h2>
            <p style="font-size: 1.5rem;">Ahora eres Nivel <span id="new-level-num">2</span></p>
            <button class="btn btn-primary" onclick="closeLevelUp()" style="margin-top: 2rem; font-size: 1.2rem;">¡Genial!</button>
        </div>
    </div>
"""
content = content.replace('</body>', modal_html + '\n</body>')

# 5. Inject JS Logic
js_logic = """
        // ============================================
        // GAME LOGIC (RPG SYSTEM)
        // ============================================
        const playerStats = {
            xp: 0,
            level: 1,
            xpToNext: 1000
        };

        function loadStats() {
            const saved = localStorage.getItem('jp_rpg_stats');
            if (saved) {
                const parsed = JSON.parse(saved);
                playerStats.xp = parsed.xp || 0;
                playerStats.level = parsed.level || 1;
                playerStats.xpToNext = parsed.xpToNext || 1000;
            }
            updateStatsUI();
        }

        function saveStats() {
            localStorage.setItem('jp_rpg_stats', JSON.stringify(playerStats));
        }

        function addXP(amount, element) {
            playerStats.xp += amount;
            
            // Show floating text
            if (element) {
                const rect = element.getBoundingClientRect();
                const floater = document.createElement('div');
                floater.className = 'floating-xp';
                floater.textContent = `+${amount} XP`;
                floater.style.left = `${rect.left + rect.width/2}px`;
                floater.style.top = `${rect.top}px`;
                document.body.appendChild(floater);
                setTimeout(() => floater.remove(), 1000);
            }

            // Level Up Check
            if (playerStats.xp >= playerStats.xpToNext) {
                playerStats.xp -= playerStats.xpToNext;
                playerStats.level++;
                playerStats.xpToNext = Math.floor(playerStats.xpToNext * 1.2);
                showLevelUp();
            }

            saveStats();
            updateStatsUI();
        }

        function updateStatsUI() {
            document.getElementById('player-level').textContent = playerStats.level;
            document.getElementById('xp-text').textContent = `${Math.floor(playerStats.xp)} / ${playerStats.xpToNext}`;
            const percentage = (playerStats.xp / playerStats.xpToNext) * 100;
            document.getElementById('xp-fill').style.width = `${percentage}%`;
        }

        function showLevelUp() {
            document.getElementById('new-level-num').textContent = playerStats.level;
            document.getElementById('level-up-modal').classList.add('active');
            
            // Confetti effect (simple unicode rain)
            // ... (omitted for brevity)
        }

        function closeLevelUp() {
            document.getElementById('level-up-modal').classList.remove('active');
        }

        // Initialize
        loadStats();
"""

# Inject JS before existing script closing or at the start of script
# Let's put it right after "const courseData = ...;" block ends
# Find the end of courseData
match = re.search(r'const courseData = \{[\s\S]*?\};\s*', content)
if match:
    end_pos = match.end()
    content = content[:end_pos] + "\n" + js_logic + "\n" + content[end_pos:]

# 6. Hook XP into actions
# Hook into Flashcard "Dominated" (markKnown)
# Find function markKnown(btn, id)
# It's not explicitly defined in the file I read before, but logic is likely inline or inside renderLesson
# Wait, I need to check where markKnown is defined.
# I'll add a global override or hook if I can find it.
# Assuming I need to add markKnown function if it's not there, or modify it.

# Let's assume the previous code generated renderLesson with inline onclicks or similar.
# I'll search for 'markKnown' in the content to see how it's implemented.
# If not found, I'll assume I need to implement it.

# Actually, in the `renderLesson` function (which I haven't fully seen but I know it exists), 
# there should be logic for buttons.
# I'll use regex to find the button click handler for "Ya la sé" (Dominated).

# Replace the "Ya la sé" button onclick to include addXP
# Button likely has class "card-btn know" or similar.
# Pattern: onclick="markAsKnown(this, '...')"
# Let's just find the text "Ya la sé" and see the surrounding HTML.

# Actually, I'll just add the `markAsKnown` function to the JS block I'm injecting, 
# ensuring it calls addXP.

js_extras = """
        function markAsKnown(btn, cardId) {
            // Visual feedback
            const card = btn.closest('.flashcard');
            if (!card.classList.contains('known')) {
                card.classList.add('known');
                addXP(50, btn); // Add 50 XP
                
                // Update progress
                updateProgress(1); // Assume this function exists or I need to find it
            }
            btn.disabled = true;
            btn.textContent = '¡Dominada!';
            
            // Save to local storage (simple version)
            const known = JSON.parse(localStorage.getItem('jp_known_cards') || '[]');
            if (!known.includes(cardId)) {
                known.push(cardId);
                localStorage.setItem('jp_known_cards', JSON.stringify(known));
            }
        }
"""
# Append this to JS logic

# 7. Modify Flashcard HTML generation to use markAsKnown
# I need to find where the flashcards are generated. 
# It's likely in `renderLesson()` function.
# I'll use regex to replace the button generation.
# Look for `<button class="card-btn know"`...

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected base RPG logic.")
