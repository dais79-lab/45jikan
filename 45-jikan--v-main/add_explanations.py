import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update startLesson to pass 'explanation'
# I need to capture `explanation` from vocab and pass it to question object.
# Also remove "Opción Extra" logic by ensuring getDistractors works well (it already does, but let's be safe).

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
            // Fallback if pool is empty (shouldn't happen with full data)
            if (pool.length < count) {
                pool.push("Respuesta A", "Respuesta B", "Respuesta C"); 
            }
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
                audio: v.audioText,
                explanation: v.explanation || "Repasa el vocabulario de la lección."
            });
        });

        // Exercises
        if (lesson.exercises) {
            lesson.exercises.forEach(ex => {
                queue.push({
                    type: 'exercise',
                    prompt: ex.question,
                    correct: ex.options.find(o => o.correct).text,
                    options: ex.options.map(o => o.text),
                    audio: null,
                    explanation: "Revisa la gramática de esta sección."
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

content = re.sub(r"function startLesson\(id\) \{[\s\S]*?\}\s*(?=let selectedOption)", new_startLesson + "\n\n    ", content)

# 2. Update renderQuestion to remove "Opción Extra" loop
# And handle option count gracefully.

new_renderQuestion = """
    function renderQuestion() {
        if (gameState.currentIndex >= gameState.currentQueue.length) {
            finishLesson();
            return;
        }

        currentQuestion = gameState.currentQueue[gameState.currentIndex];
        const body = document.getElementById('game-body');
        const progress = (gameState.currentIndex / gameState.currentQueue.length) * 100;
        document.getElementById('game-progress').style.width = `${progress}%`;
        
        document.getElementById('check-btn').disabled = true;
        document.getElementById('feedback-sheet').classList.remove('correct', 'wrong');
        document.getElementById('feedback-sheet').style.transform = 'translateY(100%)';
        selectedOption = null;

        let html = `<div class="question-text">${currentQuestion.prompt}</div>`;
        
        // Ensure unique options
        let opts = [...new Set(currentQuestion.options)];
        // Shuffle
        opts = opts.sort(() => 0.5 - Math.random());

        html += `<div class="options-grid">`;
        opts.forEach(opt => {
            html += `<div class="option-card" onclick="selectOption(this, '${opt.replace(/'/g, "\'")}')">${opt}</div>`;
        });
        html += `</div>`;

        body.innerHTML = html;
    }
"""

content = re.sub(r"function renderQuestion\(\) \{[\s\S]*?\}\s*(?=window\.selectOption)", new_renderQuestion + "\n\n    ", content)


# 3. Update checkAnswer to show explanation
# We'll append explanation to feedbackText

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
            feedbackText.innerHTML = "<div>¡Golpe Crítico!</div>";
            new Audio('duolingo-correct.mp3').play().catch(e => {});
            
            // Auto advance after 1.5 seconds
            setTimeout(() => {
                nextQuestion();
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
            
            gameState.hearts--;
            updateStats();
            saveProgress();
            
            if (gameState.hearts <= 0) {
                setTimeout(() => {
                    alert("¡Has sido derrotado! (Sin vidas)");
                    closeGame();
                }, 2000); // Give time to read
            }
        }
    }
"""

content = re.sub(r"window\.checkAnswer = function\(\) \{[\s\S]*?\}\s*(?=window\.nextQuestion)", new_checkAnswer + "\n\n    ", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added explanations and removed 'Opción Extra'.")
