import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

missing_html = """
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
                    <div class="xp-reward" style="font-size: 2rem; font-weight: 800;">+50</div>
                </div>
            </div>
            <button class="check-btn" onclick="closeCompletion()" style="width: 100%;">CONTINUAR</button>
        </div>
    </div>
"""

# Insert before the first <script> tag (ignoring the error handler script if it's in head, but we are looking at body)
# The previous read showed <script> at line 674, which is the main script.
# We want to insert before that.

# We can match `class="bottom-nav"` end and insert after it.
# Or just search for `<script>` and insert before it (but only the one that starts `const courseData`).

# Let's target `<script>\nconst courseData`.
content = re.sub(r'(<script>\s*const courseData)', missing_html + r'\n\1', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored missing Game Overlay HTML.")
