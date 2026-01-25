import os
import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Google Font
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

        /* Header Stats */
        .player-stats {
            background: rgba(0,0,0,0.2);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            gap: 1rem;
            margin-top: 1rem;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .level-badge {
            background: var(--level-bg);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 12px;
            font-weight: bold;
            box-shadow: 0 3px 0 rgba(0,0,0,0.2);
            font-size: 1.1rem;
        }

        .xp-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: white;
            font-weight: bold;
        }

        .xp-bar-mini {
            width: 120px;
            height: 12px;
            background: rgba(0,0,0,0.3);
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .xp-fill-mini {
            height: 100%;
            background: var(--xp-bg);
            width: 0%;
            transition: width 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
            box-shadow: 0 0 5px var(--xp-bg);
        }

        /* Floating XP Animation */
        .floating-xp {
            position: fixed;
            color: #ff9f1c;
            font-weight: 800;
            font-size: 1.5rem;
            pointer-events: none;
            animation: floatUp 1s ease-out forwards;
            z-index: 9999;
            text-shadow: 2px 2px 0px white, -1px -1px 0 white;
        }

        @keyframes floatUp {
            0% { transform: translateY(0) scale(1); opacity: 1; }
            50% { transform: translateY(-30px) scale(1.2); opacity: 1; }
            100% { transform: translateY(-60px) scale(1.5); opacity: 0; }
        }

        /* Level Up Modal */
        .level-up-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.85);
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
            border: 8px solid var(--level-bg);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .level-up-modal.active .level-up-content {
            transform: scale(1);
        }

        .level-up-title {
            font-size: 3rem;
            color: var(--level-bg);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            text-shadow: 2px 2px 0 #ddd;
        }

        /* Card flip animation 3D */
        .flashcard {
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
        }
        
        .flashcard.flipped {
            transform: rotateY(180deg);
        }

        .card-front, .card-back {
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
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
        
        .lesson-card-item {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 5px solid var(--secondary);
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        
        .lesson-card-item:hover {
            transform: translateX(5px);
        }
"""

if "/* Gameification Styles */" not in content:
    content = content.replace('</style>', new_css + '\n    </style>')

# 3. Inject Header Stats
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
content = re.sub(r'<header>[\s\S]*?</header>', header_html, content)

# 4. Inject Level Up Modal
modal_html = """
    <!-- Level Up Modal -->
    <div class="level-up-modal" id="level-up-modal">
        <div class="level-up-content">
            <div style="font-size: 5rem; animation: bounce 1s infinite;">🎉</div>
            <h2 class="level-up-title">¡SUBIDA DE NIVEL!</h2>
            <p style="font-size: 1.5rem; color: #666;">¡Felicidades!</p>
            <p style="font-size: 2rem; font-weight: bold; margin: 1rem 0;">Nivel <span id="new-level-num">2</span></p>
            <button class="btn btn-primary" onclick="closeLevelUp()" style="margin-top: 1rem; font-size: 1.2rem; padding: 0.8rem 2rem;">¡Genial!</button>
        </div>
    </div>
    <style>
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    </style>
"""
content = content.replace('</body>', modal_html + '\n</body>')

# 5. Inject Base JS
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
            const levelEl = document.getElementById('player-level');
            const xpTextEl = document.getElementById('xp-text');
            const xpFillEl = document.getElementById('xp-fill');
            
            if(levelEl) levelEl.textContent = playerStats.level;
            if(xpTextEl) xpTextEl.textContent = `${Math.floor(playerStats.xp)} / ${playerStats.xpToNext}`;
            if(xpFillEl) {
                const percentage = Math.min((playerStats.xp / playerStats.xpToNext) * 100, 100);
                xpFillEl.style.width = `${percentage}%`;
            }
        }

        function showLevelUp() {
            document.getElementById('new-level-num').textContent = playerStats.level;
            document.getElementById('level-up-modal').classList.add('active');
            
            // Play sound if available
            // const audio = new Audio('levelup.mp3'); audio.play().catch(e=>{});
        }

        window.closeLevelUp = function() {
            document.getElementById('level-up-modal').classList.remove('active');
        }

        // Initialize on load
        document.addEventListener('DOMContentLoaded', loadStats);
        
        // Global listener for flashcards
        document.addEventListener('click', function(e) {
            if (e.target && e.target.classList.contains('know') && !e.target.disabled) {
                // It's a "Ya la sé" button
                addXP(50, e.target);
            }
        });
"""

# Insert JS logic at the end of script block
content = content.replace('</script>', js_logic + '\n    </script>')

# 6. Inject XP calls into Minigames (Regex Replacements)

# Matching Game
# matches++; -> matches++; addXP(20, selectedCard);
content = re.sub(
    r'(matches\+\+;)', 
    r'\1 addXP(20, selectedCard);', 
    content
)

# Dictation Game
# score++; -> score++; addXP(30, btnElement);
content = re.sub(
    r'(score\+\+;)(\s*btnElement\.style\.background)', 
    r'\1 addXP(30, btnElement);\2', 
    content
)

# Sentence Game
# score++; -> score++; addXP(40, document.getElementById('sentence-display'));
content = re.sub(
    r'(score\+\+;)(\s*feedback\.innerHTML)', 
    r'\1 addXP(40, document.getElementById("sentence-display"));\2', 
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Gameified successfully.")
