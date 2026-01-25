import os
import re
import json

root_dir = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15"
html_path = os.path.join(root_dir, "prueba japones material.html")
json_path = os.path.join(root_dir, "extracted_data.json")
output_path = os.path.join(root_dir, "juego_interactivo.html")

print("Reading files...")
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Update courseData
# Find the block: const courseData = { ... };
# We use regex with DOTALL. It might be tricky if braces are nested, 
# but usually in this file it's a top level definition.
# Pattern: const courseData = \{.*?\}; (greedy might be an issue if there are other consts)
# Better: Find "const courseData =" and then find the matching closing brace?
# Or just simpler: The file has specific structure.
# Let's try to replace the known structure from the file I read earlier.
# The original file has:
# const courseData = {
#     lessons: [
#         {
#             id: "L1",
# ...
#     ]
# };

# I'll construct the new JS string
new_js_data = "const courseData = " + json.dumps(data, ensure_ascii=False, indent=4) + ";"

# Replace using regex
# Match from "const courseData = {" to "};"
# Be careful not to match too much.
html_content = re.sub(
    r'const courseData = \{[\s\S]*?\}\s*;\s*(?=\/\/\s*={10,})', 
    new_js_data + "\n\n", 
    html_content
)

# Fallback if regex didn't match perfectly due to whitespace or comments
if "const courseData = {" in html_content and "Lección 1: Kanji Básicos" in html_content:
    # If it still looks like the old one (check by content), try a simpler replacement
    # or just brute force replace the known L1 string if regex failed.
    pass

# 2. Update Lesson Select Options
# <select id="lesson-select" aria-label="Seleccionar lección">
#     <option value="L1">Lección 1: Kanji Básicos (水火食飲魚)</option>
# </select>

new_options = ""
for lesson in data['lessons']:
    new_options += f'                <option value="{lesson["id"]}">{lesson["title"]}</option>\n'

select_pattern = r'(<select id="lesson-select"[^>]*>)([\s\S]*?)(</select>)'
html_content = re.sub(select_pattern, f'\\1\n{new_options}            \\3', html_content)

# 3. Update initial lesson ID
# let currentLesson = "L1"; -> let currentLesson = "L4";
first_lesson_id = data['lessons'][0]['id']
html_content = re.sub(r'let currentLesson = "L1";', f'let currentLesson = "{first_lesson_id}";', html_content)

# Write output
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully created {output_path}")
