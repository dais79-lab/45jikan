import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix CSS for feedback sheet visibility
# Find the .feedback-sheet.correct block and add transform: translateY(0);
# Or just replace the whole block.

css_fix = """
        .feedback-sheet.correct {
            background: #d7ffb8;
            color: var(--duo-green-shadow);
            transform: translateY(0);
        }

        .feedback-sheet.wrong {
            background: #ffdfe0;
            color: var(--duo-red-shadow);
            transform: translateY(0);
        }
"""

# Replace the existing blocks
# Pattern: .feedback-sheet.correct \{[\s\S]*?\}[\s\S]*?.feedback-sheet.wrong \{[\s\S]*?\}

pattern = r"\.feedback-sheet\.correct \{[\s\S]*?\}\s*\.feedback-sheet\.wrong \{[\s\S]*?\}"
content = re.sub(pattern, css_fix, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed CSS to make feedback sheet visible.")
