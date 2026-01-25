import os
import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new implementation
new_implementation = r"""
        // ============================================
        // GAME 2: DICTATION (MULTIPLE CHOICE)
        // ============================================
        function startDictationGame() {
            const lesson = courseData.lessons.find(l => l.id === currentLesson);
            const vocab = lesson.vocabulary;
            
            let currentWord = 0;
            let score = 0;
            
            function showWord() {
                if (currentWord >= vocab.length) {
                    endDictationGame(score, vocab.length);
                    return;
                }
                
                const word = vocab[currentWord];
                
                // Generate options
                let options = [word.kana];
                const distractors = vocab.filter(v => v.kana !== word.kana);
                
                // Pick unique distractors
                const uniqueDistractors = [...new Set(distractors.map(d => d.kana))];
                const shuffledDistractors = uniqueDistractors.sort(() => 0.5 - Math.random());
                
                if (shuffledDistractors.length >= 2) {
                    options.push(shuffledDistractors[0]);
                    options.push(shuffledDistractors[1]);
                } else {
                    // Fallback distractors if not enough vocab
                    options.push("あいうえお");
                    options.push("かきくけこ");
                }
                
                // Shuffle options
                options = options.sort(() => 0.5 - Math.random());
                
                const content = document.getElementById('game-content');
                
                content.innerHTML = `
                    <h2 style="margin-bottom: 1rem; color: var(--primary);">🎤 Dictado en Hiragana</h2>
                    <p style="margin-bottom: 1rem;">Escucha la palabra y selecciona la escritura correcta.</p>
                    <div style="text-align: center; margin: 2rem 0;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">${word.kanji}</div>
                        <button class="btn btn-primary" onclick="speakText('${word.audioText}', 'ja')" style="font-size: 1.2rem;">
                            🔊 Escuchar palabra
                        </button>
                    </div>
                    
                    <div style="display: grid; gap: 1rem; margin: 2rem 0;">
                        ${options.map(opt => `
                            <button class="btn dictation-option" 
                                    style="padding: 1rem; font-size: 1.2rem; background: white; color: var(--text); border: 2px solid #ddd; width: 100%; text-align: center;"
                                    onclick="checkDictation(this, '${opt.replace(/'/g, "\\'")}')">
                                ${opt}
                            </button>
                        `).join('')}
                    </div>
                    
                    <div id="dictation-feedback" style="margin-top: 1rem; text-align: center; font-weight: 600; min-height: 1.5em;"></div>
                    <p style="text-align: center; margin-top: 1rem; color: #666;">
                        Palabra ${currentWord + 1} de ${vocab.length} | Puntos: ${score}
                    </p>
                `;
            }
            
            window.checkDictation = function(btnElement, selected) {
                const word = vocab[currentWord];
                const feedback = document.getElementById('dictation-feedback');
                const buttons = document.querySelectorAll('.dictation-option');
                
                // Disable all buttons
                buttons.forEach(btn => btn.disabled = true);
                
                if (selected === word.kana) {
                    score++;
                    btnElement.style.background = '#d4edda';
                    btnElement.style.borderColor = '#28a745';
                    feedback.innerHTML = `<span style="color: #28a745;">✓ ¡Correcto!</span>`;
                    setTimeout(() => {
                        currentWord++;
                        showWord();
                    }, 1000);
                } else {
                    btnElement.style.background = '#f8d7da';
                    btnElement.style.borderColor = '#dc3545';
                    
                    // Highlight correct answer
                    buttons.forEach(btn => {
                        if (btn.textContent.trim() === word.kana) {
                            btn.style.background = '#d4edda';
                            btn.style.borderColor = '#28a745';
                        }
                    });
                    
                    feedback.innerHTML = `<span style="color: #dc3545;">✗ Incorrecto. La respuesta era: ${word.kana}</span>`;
                    setTimeout(() => {
                        currentWord++;
                        showWord();
                    }, 2000);
                }
            };
            
            showWord();
        }

        function endDictationGame(score, total) {
            const content = document.getElementById('game-content');
            const percentage = Math.round((score / total) * 100);
            
            content.innerHTML = `
                <h2 style="margin-bottom: 1rem; color: var(--primary);">🎉 ¡Dictado Completado!</h2>
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">
                        ${percentage === 100 ? '🏆' : percentage >= 70 ? '🌟' : '📝'}
                    </div>
                    <h3 style="font-size: 2rem; margin-bottom: 0.5rem;">${score} / ${total}</h3>
                    <p style="font-size: 1.2rem; color: #666;">
                        ${percentage === 100 ? '¡Perfecto! ¡Oído agudo!' :
                          percentage >= 70 ? '¡Muy bien! Sigue así.' :
                          '¡Sigue practicando! Escuchar es clave.'}
                    </p>
                </div>
                <div style="display: flex; gap: 1rem; justify-content: center;">
                    <button class="btn btn-primary" onclick="startDictationGame()">🔄 Reintentar</button>
                    <button class="btn" onclick="openGamesModal()">← Menú de juegos</button>
                </div>
            `;
        }
"""

# Regex to find the existing block
# It starts with startDictationGame definition and ends after endDictationGame closing brace
# We need to be careful to match the whole block.
# Since we know the structure from the previous read, we can use a pattern that matches from startDictationGame up to the start of startSentenceGame.

pattern = r"function startDictationGame\(\) \{[\s\S]*?\}\s*function endDictationGame\(score, total\) \{[\s\S]*?\}\s*(?=\s*// ============================================)"

# Check if pattern matches
match = re.search(pattern, content)
if match:
    print("Found dictation game block.")
    new_content = content.replace(match.group(0), new_implementation.strip())
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated dictation game.")
else:
    print("Could not find dictation game block to replace.")
    # Fallback: try to find startSentenceGame as anchor
    start_anchor = "function startDictationGame() {"
    end_anchor = "function startSentenceGame() {"
    
    start_idx = content.find(start_anchor)
    end_idx = content.find(end_anchor)
    
    if start_idx != -1 and end_idx != -1:
        # We need to backtrack from end_idx to include the separator comments
        # But replacing strictly between functions is safer
        # Let's find the end of endDictationGame before startSentenceGame
        # It usually ends with "}" followed by comments.
        
        # Actually, replacing from start_idx to end_idx-1 (roughly) might work if we include the separator in new_implementation
        # Let's just replace the chunk
        old_chunk = content[start_idx:end_idx]
        # We need to keep the separator for startSentenceGame
        # The separator is usually before the function definition.
        
        # Let's look for the separator before startSentenceGame
        separator = "// ============================================\n        // GAME 3: SENTENCE ORDERING"
        sep_idx = content.find(separator)
        
        if sep_idx != -1:
            old_chunk = content[start_idx:sep_idx]
            new_content = content[:start_idx] + new_implementation + "\n\n        " + content[sep_idx:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully updated dictation game using offsets.")
        else:
            print("Could not find separator for replacement.")

