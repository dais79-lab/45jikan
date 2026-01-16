import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the "CONTINUAR" button to "SIGUIENTE" in HTML
# The button is at line ~699 in the read output.
# <button class="check-btn" onclick="nextQuestion()" style="margin: 0; background: white; color: inherit; border: 2px solid rgba(0,0,0,0.1);">CONTINUAR</button>
# I will use regex to find this specific button and replace text.
# Be careful with spacing.

button_regex = r'(<button class="check-btn" onclick="nextQuestion\(\)"[^>]*>)\s*CONTINUAR\s*(</button>)'
content = re.sub(button_regex, r'\1SIGUIENTE\2', content)

# 2. Update checkAnswer to:
# - Auto-advance if correct (already done, but let's ensure it's kept).
# - If wrong, show explanation and keep the sheet up (user clicks SIGUIENTE).
# - Make sure the SIGUIENTE button is visible.
# In my previous code, I injected `feedbackText.innerHTML`.
# The button is OUTSIDE feedbackText (it's a sibling).
# So I don't need to inject the button again. I just need to make sure I don't hide it.
# The sheet slides up via CSS class.

# Refined checkAnswer:
# - Correct: Show "Golpe Crítico", play sound, auto-advance.
# - Wrong: Show "Fallaste" + Explanation, play sound. Wait for user.

new_checkAnswer = """
    window.checkAnswer = function() {
        if (!selectedOption) return;
        
        const isCorrect = (selectedOption === currentQuestion.correct);
        const feedback = document.getElementById('feedback-sheet');
        const feedbackText = document.getElementById('feedback-text');
        const continueBtn = feedback.querySelector('button'); // The SIGUIENTE button
        
        // Disable interactions
        document.querySelectorAll('.option-card').forEach(c => c.style.pointerEvents = 'none');
        document.getElementById('check-btn').disabled = true;

        document.querySelectorAll('.option-card').forEach(c => {
            if (c.textContent === currentQuestion.correct) c.classList.add('correct');
            else if (c.classList.contains('selected') && !isCorrect) c.classList.add('wrong');
        });

        if (isCorrect) {
            feedback.className = 'feedback-sheet correct';
            feedbackText.innerHTML = "<div>¡Golpe Crítico!</div>";
            new Audio('duolingo-correct.mp3').play().catch(e => {});
            
            // Hide the manual button for correct answers to avoid confusion if auto-advancing
            if(continueBtn) continueBtn.style.display = 'none';

            // Auto advance after 1.5 seconds
            setTimeout(() => {
                nextQuestion();
                // Reset button visibility for next time
                if(continueBtn) continueBtn.style.display = 'block';
            }, 1500);
        } else {
            feedback.className = 'feedback-sheet wrong';
            // Show correction + Explanation
            feedbackText.innerHTML = `
                <div style="margin-bottom:10px;">Fallaste. Era: <strong>${currentQuestion.correct}</strong></div>
                <div style="font-size: 0.9rem; font-weight: normal; background: rgba(0,0,0,0.1); padding: 10px; border-radius: 8px;">
                    💡 ${currentQuestion.explanation || "Inténtalo de nuevo."}
                </div>
            `;
            new Audio('duolingo-wrong.mp3').play().catch(e => {});
            
            // Ensure button is visible for wrong answers
            if(continueBtn) {
                continueBtn.style.display = 'block';
                // Improve styling for visibility on red background
                continueBtn.style.background = 'white';
                continueBtn.style.color = '#d42020'; // Red text
                continueBtn.style.border = '2px solid rgba(0,0,0,0.1)';
            }
            
            gameState.hearts--;
            updateStats();
            saveProgress();
            
            if (gameState.hearts <= 0) {
                // Hide next button if game over
                if(continueBtn) continueBtn.style.display = 'none';
                setTimeout(() => {
                    alert("¡Has sido derrotado! (Sin vidas)");
                    closeGame();
                }, 2000); 
            }
        }
    }
"""

content = re.sub(r"window\.checkAnswer = function\(\) \{[\s\S]*?\}\s*(?=window\.nextQuestion)", new_checkAnswer + "\n\n    ", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated button to 'SIGUIENTE' and refined wrong answer flow.")
