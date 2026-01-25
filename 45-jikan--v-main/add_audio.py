import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new checkAnswer function with audio
new_checkAnswer = """
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
            feedbackText.textContent = "¡Golpe Crítico!";
            new Audio('duolingo-correct.mp3').play().catch(e => console.log('Audio error:', e));
        } else {
            feedback.className = 'feedback-sheet wrong';
            feedbackText.textContent = `Fallaste. Era: ${currentQuestion.correct}`;
            new Audio('duolingo-wrong.mp3').play().catch(e => console.log('Audio error:', e));
            
            gameState.hearts--;
            updateStats();
            saveProgress();
            if (gameState.hearts <= 0) {
                // Delay alert slightly to let sound play
                setTimeout(() => {
                    alert("¡Has sido derrotado! (Sin vidas)");
                    closeGame();
                }, 500);
                return;
            }
        }
    }
"""

# Replace the existing function using regex
# Pattern matches from `window.checkAnswer = function() {` until `window.nextQuestion =`
# Be careful with the closing brace of the function.
# The structure is:
# window.checkAnswer = function() { ... }
# window.nextQuestion = ...

pattern = r"window\.checkAnswer = function\(\) \{[\s\S]*?\}\s*(?=window\.nextQuestion)"
content = re.sub(pattern, new_checkAnswer + "\n\n    ", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added audio feedback to checkAnswer.")
