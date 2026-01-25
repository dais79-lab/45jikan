import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS Replacement for Dark Mode / Better Contrast
new_css = """
        :root {
            --duo-green: #58cc02;
            --duo-green-shadow: #46a302;
            --duo-red: #ff4b4b;
            --duo-red-shadow: #d42020;
            --duo-blue: #1cb0f6;
            --duo-blue-shadow: #1899d6;
            --duo-yellow: #ffc800;
            --duo-yellow-shadow: #e5a500;
            
            /* Dark RPG Theme */
            --bg-color: #131f24; 
            --sidebar-bg: #131f24;
            --card-bg: #202f36;
            --text-color: #ffffff;
            --text-muted: #8b9dad;
            --border-color: #37464f;
            --hover-bg: #2a3b47;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Fredoka', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            overflow: hidden;
        }

        /* --- Header --- */
        .app-header {
            height: 60px;
            border-bottom: 2px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            background: var(--bg-color);
            z-index: 100;
        }

        .stats-container {
            display: flex;
            gap: 20px;
        }

        .stat-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            color: var(--text-muted);
            font-size: 1.1rem;
        }
        
        .stat-item.active { color: var(--duo-yellow); }
        .stat-item.hearts { color: var(--duo-red); }

        /* --- Layout --- */
        .main-container {
            display: flex;
            height: calc(100vh - 60px);
        }

        .sidebar {
            width: 250px;
            border-right: 2px solid var(--border-color);
            padding: 20px;
            background: var(--sidebar-bg);
            display: none;
        }
        
        @media (min-width: 768px) {
            .sidebar { display: block; }
        }

        .content-area {
            flex: 1;
            overflow-y: auto;
            position: relative;
            background-color: var(--bg-color);
            background-image: radial-gradient(var(--border-color) 1px, transparent 1px);
            background-size: 20px 20px;
        }

        /* --- Sidebar Items --- */
        .sidebar-item {
            padding: 15px;
            margin: 10px 0;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 700;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.2s;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 1px;
            border: 2px solid transparent;
        }

        .sidebar-item:hover {
            background: var(--hover-bg);
        }

        .sidebar-item.active {
            background: rgba(28, 176, 246, 0.15);
            color: var(--duo-blue);
            border-color: var(--duo-blue-shadow);
        }

        /* Avatar */
        .avatar-container {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: var(--card-bg);
            border-radius: 20px;
            border: 2px solid var(--border-color);
        }

        .avatar-img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #eee;
            margin-bottom: 10px;
            border: 3px solid var(--duo-blue);
        }

        .level-badge {
            background: var(--duo-blue);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.8rem;
            display: inline-block;
            font-weight: bold;
            margin-top: 5px;
            box-shadow: 0 4px 0 var(--duo-blue-shadow);
        }

        /* --- Lesson Path --- */
        .lesson-path {
            padding: 40px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 40px;
            max-width: 500px;
            margin: 0 auto;
        }

        .unit-header {
            background: var(--duo-green);
            color: white;
            width: 90%;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 6px 0 var(--duo-green-shadow);
            border: 2px solid rgba(0,0,0,0.1);
        }

        .lesson-node {
            width: 80px;
            height: 80px;
            background: var(--duo-green);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 8px 0 var(--duo-green-shadow);
            cursor: pointer;
            position: relative;
            transition: transform 0.1s;
            z-index: 10;
        }

        .lesson-node:active {
            transform: translateY(6px);
            box-shadow: 0 2px 0 var(--duo-green-shadow);
        }

        .lesson-node.locked {
            background: var(--card-bg);
            box-shadow: 0 8px 0 var(--border-color);
            cursor: not-allowed;
            border: 2px solid var(--border-color);
        }

        .lesson-title {
            position: absolute;
            top: 95px;
            background: var(--card-bg);
            padding: 8px 12px;
            border-radius: 12px;
            border: 2px solid var(--border-color);
            font-size: 0.9rem;
            white-space: nowrap;
            display: none;
            z-index: 20;
            color: var(--text-color);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        
        .lesson-node:hover .lesson-title {
            display: block;
        }

        /* --- Views --- */
        .view-section {
            display: none;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
        }

        .view-section.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Vocab Grid */
        .vocab-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 20px;
        }

        .vocab-card {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 6px 0 var(--border-color);
            transition: transform 0.2s;
        }
        
        .vocab-card:hover {
            transform: translateY(-5px);
        }
        
        .vocab-jp { font-size: 1.8rem; margin-bottom: 10px; color: var(--duo-blue); font-weight: bold; }
        .vocab-es { font-size: 1rem; color: var(--text-muted); }

        /* Shop Items */
        .shop-item {
            display: flex;
            align-items: center;
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 6px 0 var(--border-color);
        }

        .shop-icon { font-size: 3rem; margin-right: 25px; }
        .shop-info { flex: 1; }
        .shop-title { font-weight: bold; font-size: 1.2rem; margin-bottom: 5px; }
        .shop-desc { font-size: 1rem; color: var(--text-muted); }
        
        .buy-btn {
            background: var(--bg-color);
            border: 2px solid var(--border-color);
            padding: 12px 25px;
            border-radius: 12px;
            font-weight: bold;
            color: var(--text-muted);
            cursor: pointer;
            box-shadow: 0 4px 0 var(--border-color);
            transition: all 0.2s;
        }
        
        .buy-btn:active { transform: translateY(4px); box-shadow: none; }
        
        .buy-btn.can-afford {
            background: var(--duo-blue);
            color: white;
            border-color: var(--duo-blue-shadow);
            box-shadow: 0 4px 0 var(--duo-blue-shadow);
        }

        /* --- Game Overlay --- */
        .game-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-color);
            z-index: 2000;
            display: none;
            flex-direction: column;
        }
        
        .game-overlay.active { display: flex; }

        .game-header {
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 20px;
            max-width: 1000px;
            width: 100%;
            margin: 0 auto;
        }

        .close-btn {
            font-size: 2rem;
            cursor: pointer;
            color: var(--text-muted);
        }

        .progress-bar-container {
            flex: 1;
            height: 16px;
            background: var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: var(--duo-green);
            width: 0%;
            transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 8px;
            box-shadow: 0 2px 0 rgba(255,255,255,0.2) inset;
        }

        .game-body {
            flex: 1;
            padding: 20px;
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .question-text {
            font-size: 2rem;
            margin-bottom: 3rem;
            text-align: center;
            font-weight: bold;
            color: var(--text-color);
        }

        .options-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 600px) {
            .options-grid { grid-template-columns: 1fr; }
        }

        .option-card {
            border: 2px solid var(--border-color);
            background: var(--card-bg);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.1s;
            box-shadow: 0 4px 0 var(--border-color);
            font-size: 1.2rem;
            color: var(--text-color);
        }

        .option-card:active {
            transform: translateY(4px);
            box-shadow: none;
        }

        .option-card.selected {
            border-color: var(--duo-blue);
            background: rgba(28, 176, 246, 0.2);
            color: var(--duo-blue);
            box-shadow: 0 4px 0 var(--duo-blue-shadow);
        }

        .option-card.correct {
            border-color: var(--duo-green);
            background: rgba(88, 204, 2, 0.2);
            color: var(--duo-green);
        }
        
        .option-card.wrong {
            border-color: var(--duo-red);
            background: rgba(255, 75, 75, 0.2);
            color: var(--duo-red);
        }

        .game-footer {
            padding: 30px;
            border-top: 2px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-color);
        }

        .check-btn {
            background: var(--duo-green);
            color: white;
            border: none;
            padding: 16px 40px;
            border-radius: 16px;
            font-weight: 800;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            box-shadow: 0 6px 0 var(--duo-green-shadow);
            cursor: pointer;
            width: 100%;
            max-width: 250px;
            margin-left: auto;
            transition: filter 0.2s;
        }
        
        .check-btn:hover {
            filter: brightness(1.1);
        }
        
        .check-btn:disabled {
            background: var(--border-color);
            color: var(--text-muted);
            box-shadow: none;
            cursor: default;
            filter: none;
        }

        /* --- Feedback Sheet --- */
        .feedback-sheet {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 40px;
            transform: translateY(100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 2001;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        }

        .feedback-sheet.correct {
            background: #d7ffb8;
            color: var(--duo-green-shadow);
        }

        .feedback-sheet.wrong {
            background: #ffdfe0;
            color: var(--duo-red-shadow);
        }

        .feedback-content {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

"""

# Regex replacement for CSS
# We replace content between <style> and </style>
content = re.sub(r'<style>[\s\S]*?</style>', f'<style>{new_css}</style>', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied Dark Mode RPG Theme.")
