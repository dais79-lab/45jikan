import re
import json

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Improved checkAnswer logic (Auto-advance on correct)
# I will rewrite the checkAnswer function.
new_checkAnswer = """
    window.checkAnswer = function() {
        if (!selectedOption) return;
        
        const isCorrect = (selectedOption === currentQuestion.correct);
        const feedback = document.getElementById('feedback-sheet');
        const feedbackText = document.getElementById('feedback-text');
        
        // Disable interactions
        document.querySelectorAll('.option-card').forEach(c => c.style.pointerEvents = 'none');
        document.getElementById('check-btn').disabled = true;

        document.querySelectorAll('.option-card').forEach(c => {
            if (c.textContent === currentQuestion.correct) c.classList.add('correct');
            else if (c.classList.contains('selected') && !isCorrect) c.classList.add('wrong');
        });

        if (isCorrect) {
            feedback.className = 'feedback-sheet correct';
            feedbackText.textContent = "¡Golpe Crítico!";
            new Audio('duolingo-correct.mp3').play().catch(e => {});
            
            // Auto advance after 1.5 seconds
            setTimeout(() => {
                nextQuestion();
            }, 1500);
        } else {
            feedback.className = 'feedback-sheet wrong';
            feedbackText.textContent = `Fallaste. Era: ${currentQuestion.correct}`;
            new Audio('duolingo-wrong.mp3').play().catch(e => {});
            
            gameState.hearts--;
            updateStats();
            saveProgress();
            
            // Re-enable continue button in feedback sheet for incorrect answers
            // (Wait for user to click "CONTINUAR")
            
            if (gameState.hearts <= 0) {
                setTimeout(() => {
                    alert("¡Has sido derrotado! (Sin vidas)");
                    closeGame();
                }, 1000);
            }
        }
    }
"""

# Replace checkAnswer
content = re.sub(r"window\.checkAnswer = function\(\) \{[\s\S]*?\}\s*(?=window\.nextQuestion)", new_checkAnswer + "\n\n    ", content)

# 2. Improved startLesson logic (Better distractors)
# I need to modify startLesson to pick random wrong answers from OTHER lessons or the same lesson.
# I'll inject a helper function `getDistractors`.

distractor_helper = """
    function getDistractors(correctAnswer, count) {
        // Collect all possible answers (Spanish meanings)
        let allAnswers = [];
        courseData.lessons.forEach(l => {
            if(l.vocabulary) l.vocabulary.forEach(v => {
                if(v.es && v.es !== correctAnswer && v.kanji !== '（こたえ）') allAnswers.push(v.es);
            });
        });
        
        // Shuffle and pick unique
        allAnswers = allAnswers.sort(() => 0.5 - Math.random());
        return allAnswers.slice(0, count);
    }
"""

# Inject helper before startLesson
# Find startLesson definition
# Pattern: window.startLesson = ... or function startLesson...
# In previous steps it was `function startLesson(id) {` inside the script block?
# No, in `rpg_duo_merge.py` I used `function startLesson(id)`.
# Let's find `function startLesson` and insert helper before it.

# Update startLesson to use getDistractors
new_startLesson = """
    function startLesson(id) {
        gameState.currentLessonId = id;
        const lesson = courseData.lessons.find(l => l.id === id);
        let queue = [];
        
        // Helper for distractors
        const getDistractors = (correct, count) => {
            let pool = [];
            courseData.lessons.forEach(l => {
                if(l.vocabulary) l.vocabulary.forEach(v => {
                    if(v.es && v.es !== correct && v.kanji !== '（こたえ）') pool.push(v.es);
                });
            });
            return pool.sort(() => 0.5 - Math.random()).slice(0, count);
        };

        // Vocab
        lesson.vocabulary.forEach(v => {
            if (v.kanji === '（こたえ）') return;
            const distractors = getDistractors(v.es, 3);
            queue.push({
                type: 'vocab_mc',
                prompt: `¿Qué significa "${v.kanji}"?`,
                correct: v.es,
                options: [v.es, ...distractors], 
                audio: v.audioText
            });
        });

        // Exercises
        if (lesson.exercises) {
            lesson.exercises.forEach(ex => {
                // If options are provided in data, use them.
                // If they are placeholders, maybe generate? 
                // The current data has options.
                queue.push({
                    type: 'exercise',
                    prompt: ex.question,
                    correct: ex.options.find(o => o.correct).text,
                    options: ex.options.map(o => o.text),
                    audio: null
                });
            });
        }
        
        queue = queue.sort(() => 0.5 - Math.random());
        gameState.currentQueue = queue.slice(0, 10);
        gameState.currentIndex = 0;
        
        if (gameState.hearts <= 0) {
            alert("¡Estás herido! Visita la tienda para curarte.");
            return;
        }

        document.getElementById('game-overlay').classList.add('active');
        renderQuestion();
    }
"""

# Replace startLesson
content = re.sub(r"function startLesson\(id\) \{[\s\S]*?\}\s*(?=let selectedOption)", new_startLesson + "\n\n    ", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Implemented auto-advance and smart distractors.")
