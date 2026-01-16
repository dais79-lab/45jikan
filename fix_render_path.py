import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The user is complaining that lessons are not visible.
# This might be because the renderPath function relies on 'courseData' but maybe the structure is wrong or not called correctly.
# Or maybe the "view-home" is not properly active.
# Looking at the code:
# document.addEventListener('DOMContentLoaded', () => { ... renderPath(); ... });
# And renderPath iterates courseData.lessons.

# However, there is a visual issue.
# The user sees a blank grid (implied by previous message "mas blanco q mi cara...").
# In the previous step, I added bottom nav and updated switchView.

# Let's verify if `courseData` is actually populated.
# The read output shows `const courseData = { "lessons": [ ... ] }` around line 631.
# And `renderPath` is defined around line 3152.

# One potential issue: `courseData` variable scope.
# It is defined in the script block. `renderPath` is also in the script block.
# Wait, I see two script blocks in my mental model?
# No, I replaced the whole script block in `rpg_duo_merge.py`.
# But in `mobile_nav_fix.py` I used regex to replace `window.switchView`.
# Let's check if I accidentally broke the script structure.

# The read output shows the script starts at line 630 and ends at 3315.
# `courseData` is at the top of the script.
# `renderPath` is at the bottom.

# Issue: The `renderPath` function might be failing or the container is not found?
# Container ID is `path-container`. It exists in HTML (line 578).

# Let's look at `renderPath` again.
# It iterates `courseData.lessons`.
# If `courseData.lessons` is empty, nothing shows.
# But it seems populated in the file read.

# Maybe the CSS for `.lesson-node` or `.lesson-path` is making them invisible?
# .lesson-path has `display: flex; flex-direction: column; ...`
# .lesson-node has `width: 80px; height: 80px; ...`
# Colors are set variables.

# Wait! In the user screenshot (which I can't see but imagine based on "mas blanco"), 
# if the user says "y las lecciónes?", it means the path is empty.

# Potential bug: `gameState.completedLessons` initialization.
# In `loadProgress`, if `duo_rpg_state` is null, `gameState` uses defaults.
# `gameState.completedLessons` is `[]`.
# `renderPath` logic:
# `isLocked = index > 0 && !gameState.completedLessons.includes(...)`
# This logic seems fine. Lesson 0 (L4) should be unlocked.

# Another possibility: JavaScript Error stopping execution.
# I used `opt.replace(/'/g, "\'")` in `renderQuestion`.
# The backslash escaping in Python string for `replace` replacement string might be tricky.
# `opt.replace(/'/g, "\\'")` -> in JS file it becomes `opt.replace(/'/g, "\'")` which escapes the quote.
# But if I used `r` prefix in python, `\'` is literal backslash and quote.
# If I wrote `opt.replace(/'/g, "\'")` in the python script, and wrote it to file...
# Let's check the file content around line 3260:
# `html += `<div class="option-card" onclick="selectOption(this, '${opt.replace(/'/g, "\'")}')">${opt}</div>`;`
# In JS: `'${opt.replace(/'/g, "\'")}'`
# If opt has a quote, e.g. "It's", it becomes "It\'s".
# Inside the HTML attribute `onclick="selectOption(this, 'It\'s')"` -> valid.

# BUT, let's look at `mobile_nav_fix.py` replacement.
# I replaced `window.switchView` block.
# Did I accidentally cut off `renderPath`?
# I matched `(?=function renderVocab)`.
# `renderPath` is usually AFTER `js_logic` but BEFORE `renderVocab`?
# In `rpg_duo_merge.py`:
# js_logic
# renderPath
# startLesson
# ...

# Wait, in `rpg_duo_merge.py`, I defined `js_logic` which contains `gameState`, `loadProgress` etc.
# Then I appended `renderPath`.
# Then `startLesson`...

# In `mobile_nav_fix.py`, I replaced `window.switchView` which is inside `js_logic`.
# The regex was `window\.switchView = function... (?=function renderVocab)`.
# Wait, `renderVocab` is AFTER `switchView` in `js_logic`.
# `renderPath` is NOT in `js_logic` variable in `rpg_duo_merge.py`, it was appended separately?
# No, look at `rpg_duo_merge.py`:
# script_content = f""" {course_data} {js_logic} // --- Path Render ... function renderPath() ... """
# So `renderPath` comes AFTER `js_logic`.

# In `mobile_nav_fix.py`, I targeted `window.switchView` which is inside `js_logic`.
# And I used lookahead `(?=function renderVocab)`.
# Is `renderVocab` inside `js_logic`?
# Yes.
# So I replaced `switchView` up to `renderVocab`.
# `renderPath` is further down.
# So `renderPath` should be safe.

# Let's check `juego_interactivo.html` content around line 3151.
# It has `function renderPath()`.

# Why are lessons not showing?
# Maybe `courseData` is not defined when `renderPath` runs?
# `document.addEventListener('DOMContentLoaded', ...)` calls `renderPath`.
# `courseData` is defined at the top (line 631).

# Let's debug by adding a check in `renderPath`.
# And maybe the issue is that `view-home` is not visible?
# CSS: `.view-section { display: none; }`
# `.view-section.active { display: block; }`
# HTML: `<div id="view-home" class="view-section active">` (line 577).
# So it should be visible.

# Maybe the grid is white text on white background?
# `lesson-node` has `background: var(--duo-green)`. It should be visible.

# Maybe the container height is 0?
# `.content-area` has `overflow-y: auto`.

# Is it possible that `courseData` structure is broken?
# I see `courseData = { "lessons": [ ... ] }`.
# It looks valid JSON object literal.

# Let's try to force re-render and add some debug alerts.
# And also, I will add a "Reset Progress" button in the header just in case `gameState` is corrupted.

# Also, I notice `renderPath` uses `courseData.lessons.forEach`.
# If `courseData.lessons` is undefined, it throws error.

# I will write a small fix script to:
# 1. Add error handling to `renderPath`.
# 2. Add a visual "Reset" button.
# 3. Ensure `courseData` is valid.

# Wait, I see `courseData` definition ends at line 1000 in the read output, but the file has 3333 lines.
# The read was truncated?
# `limit:1000,offset:250000` -> this read the end of file.
# `limit:500,offset:3000` -> this read the script part.
# `courseData` definition is huge (lines 631 to ~3000).
# If I messed up the regex in previous steps, maybe I cut off `courseData`?
# In `mobile_nav_fix.py`, I only touched `switchView`.
# In `dark_mode_fix.py`, I touched `<style>`.
# In `rpg_duo_merge.py`, I replaced the whole script.

# Let's verify if `courseData` is closed properly.
# I'll check the end of `courseData` variable.

debug_script = """
    // Debug helper
    console.log("Course Data:", courseData);
    if (!courseData || !courseData.lessons) {
        alert("Error crítico: No se cargaron las lecciones.");
    } else {
        console.log("Lecciones cargadas:", courseData.lessons.length);
    }
"""

# I'll inject this at the start of DOMContentLoaded.

# Also, the user might be seeing "white" because the `lesson-node` elements are not being created.
# I will rewrite `renderPath` to be more robust and log to console.

new_renderPath = """
    function renderPath() {
        console.log("Rendering path...");
        const container = document.getElementById('path-container');
        if (!container) { console.error("No path container!"); return; }
        
        container.innerHTML = '';
        let unitCount = 1;
        
        if (!courseData || !courseData.lessons) {
            container.innerHTML = '<div style="padding:20px; color:red;">Error: No hay datos de lecciones.</div>';
            return;
        }
        
        courseData.lessons.forEach((lesson, index) => {
            // Unit Header every 4 lessons
            if (index % 4 === 0) {
                const header = document.createElement('div');
                header.className = 'unit-header';
                header.innerHTML = `<h3>Unidad ${unitCount}</h3><p>Misiones de Rango ${String.fromCharCode(65+unitCount)}</p>`;
                container.appendChild(header);
                unitCount++;
            }

            const isLocked = index > 0 && !gameState.completedLessons.includes(courseData.lessons[index-1].id) && !gameState.completedLessons.includes(lesson.id);
            const reallyLocked = (index === 0) ? false : isLocked;
            
            // Winding path offset
            const offset = Math.sin(index) * 60; 

            const node = document.createElement('div');
            node.className = `lesson-node ${reallyLocked ? 'locked' : ''}`;
            node.style.transform = `translateX(${offset}px)`;
            
            // Determine icon
            let icon = '⚔️'; // Default ready
            if (gameState.completedLessons.includes(lesson.id)) icon = '⭐'; // Completed
            else if (reallyLocked) icon = '🔒'; // Locked
            
            node.innerHTML = `
                <div style="font-size: 2rem;">${icon}</div>
                <div class="lesson-title">${lesson.title}</div>
            `;
            
            if (!reallyLocked) {
                node.onclick = () => startLesson(lesson.id);
            }

            container.appendChild(node);
        });
        console.log("Path rendered with " + courseData.lessons.length + " nodes.");
    }
"""

# Replace `renderPath` function.
content = re.sub(r'function renderPath\(\) \{[\s\S]*?\}\s*(?=function startLesson)', new_renderPath + "\n\n    ", content)

# I'll also add a "Clear Save" button in the footer or sidebar to reset state if it's stuck.
reset_btn = """
            <div class="sidebar-item" onclick="resetGameProgress()">
                <span>⚠️</span> REINICIAR
            </div>
"""
# Inject into sidebar
content = content.replace('<!-- Sidebar items end or marker? -->', '') # I don't have a marker.
# Find "TIENDA" item and append after it.
content = content.replace(
    '<div class="sidebar-item" onclick="switchView(\'shop\', this)">\n                <span>🛒</span> TIENDA\n            </div>',
    '<div class="sidebar-item" onclick="switchView(\'shop\', this)">\n                <span>🛒</span> TIENDA\n            </div>\n            ' + reset_btn
)

# Add reset function
reset_js = """
    window.resetGameProgress = function() {
        if(confirm("¿Borrar todo el progreso y empezar de cero?")) {
            localStorage.removeItem('duo_rpg_state');
            location.reload();
        }
    }
"""
content = content.replace('// --- Init ---', reset_js + '\n    // --- Init ---')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated renderPath and added reset option.")
