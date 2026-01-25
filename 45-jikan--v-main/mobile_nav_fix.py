import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Bottom Nav HTML
bottom_nav_html = """
    <div class="bottom-nav">
        <div class="nav-item active" onclick="switchView('home', this)">
            <div class="nav-icon">🏠</div>
            <div class="nav-label">Inicio</div>
        </div>
        <div class="nav-item" onclick="switchView('vocab', this)">
            <div class="nav-icon">📚</div>
            <div class="nav-label">Vocab</div>
        </div>
        <div class="nav-item" onclick="switchView('shop', this)">
            <div class="nav-icon">🛒</div>
            <div class="nav-label">Tienda</div>
        </div>
    </div>
"""

# Insert Bottom Nav before closing </body>
content = content.replace('</body>', bottom_nav_html + '\n</body>')

# 2. Add CSS for Bottom Nav
css_nav = """
        /* --- Bottom Navigation (Mobile) --- */
        .bottom-nav {
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 70px;
            background: var(--bg-color);
            border-top: 2px solid var(--border-color);
            justify-content: space-around;
            align-items: center;
            z-index: 1000;
            padding-bottom: 10px; /* Safe area for phones */
        }

        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            cursor: pointer;
            width: 100%;
            height: 100%;
        }

        .nav-item.active {
            color: var(--duo-blue);
        }

        .nav-icon {
            font-size: 1.5rem;
            margin-bottom: 2px;
        }

        .nav-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        @media (max-width: 768px) {
            .sidebar { display: none; }
            .bottom-nav { display: flex; }
            .main-container { height: calc(100vh - 130px); } /* Adjust for header + nav */
            .content-area { padding-bottom: 80px; }
        }
"""

content = content.replace('</style>', css_nav + '\n</style>')

# 3. Update switchView to handle both Sidebar and Bottom Nav active states
# We need to update the JS function switchView
# It currently clears .sidebar-item active class. We should clear .nav-item too.

new_switchView = """
    window.switchView = function(viewName, btnEl) {
        // Update Sidebar & Bottom Nav
        document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
        
        // Add active class to clicked element (if passed)
        if(btnEl) btnEl.classList.add('active');
        
        // Sync state: if clicked sidebar, update bottom nav too, and vice-versa
        // Simple hack: find elements by text content or icon mapping? 
        // Easier: Just set active based on viewName
        
        // Map viewName to index or selector
        const iconMap = { 'home': '🏠', 'vocab': '📚', 'shop': '🛒' };
        const iconChar = iconMap[viewName];
        
        // Highlight matching Sidebar Item
        document.querySelectorAll('.sidebar-item').forEach(el => {
            if (el.textContent.includes(iconChar)) el.classList.add('active');
        });
        
        // Highlight matching Bottom Nav Item
        document.querySelectorAll('.nav-item').forEach(el => {
            if (el.textContent.includes(iconChar)) el.classList.add('active');
        });

        // Update Views
        document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
        document.getElementById('view-' + viewName).classList.add('active');
        
        if (viewName === 'vocab') renderVocab();
    }
"""

# Replace the old switchView function
# Pattern: window.switchView = function... (until next function)
# The old function was:
#     window.switchView = function(viewName, btnEl) {
#         // Update Sidebar
#         document.querySelectorAll('.sidebar-item').forEach(el => el.classList.remove('active'));
#         if(btnEl) btnEl.classList.add('active');
#
#         // Update Views
#         document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
#         document.getElementById(`view-${viewName}`).classList.add('active');
#         
#         if (viewName === 'vocab') renderVocab();
#     }

# Regex to find and replace it
# Be careful with multiline and braces.
# We can match `window.switchView = function` until `function renderVocab`
pattern = r"window\.switchView = function\(viewName, btnEl\) \{[\s\S]*?\}\s*(?=function renderVocab)"
content = re.sub(pattern, new_switchView + "\n\n    ", content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added Mobile Navigation Bar and updated logic.")
