import os
import re
import json

# Define the directory
root_dir = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15"

# List of files to process (4 to 15)
# Files are named like 45jikan4kac.html, 45jikan10kac.html
files = [f"45jikan{i}kac.html" for i in range(4, 16)]
lessons_data = []

def clean_text(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'\s+', ' ', text).strip()

for filename in files:
    file_path = os.path.join(root_dir, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        continue
        
    print(f"Processing {filename}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract Lesson Number Correctly
    # Look for the number after '45jikan' and before 'kac'
    lesson_match = re.search(r'45jikan(\d+)kac\.html', filename)
    if not lesson_match:
        print(f"Could not parse lesson number from {filename}")
        continue
        
    lesson_num = lesson_match.group(1)
    
    # Extract Title
    title_match = re.search(r'<div class="title">(.*?)</div>', content)
    title = clean_text(title_match.group(1)) if title_match else f"Lección {lesson_num}"
    
    # Extract Subtitle/Badge
    badge_match = re.search(r'<div class="badge">(.*?)</div>', content)
    topics = clean_text(badge_match.group(1)) if badge_match else ""
    
    # Extract Dialogues
    dialog_blocks = content.split('<div class="dialog">')[1:]
    
    dialogues = []
    full_reading_text = ""
    
    for block in dialog_blocks:
        matches = re.findall(r'<div class="name">(.*?)</div>\s*<div>(.*?)</div>', block)
        for name, text in matches:
            speaker = clean_text(name).replace(':', '')
            speech = clean_text(text)
            dialogues.append({
                "speaker": speaker,
                "jp": speech,
                "romaji": "", 
                "es": "" 
            })
            full_reading_text += f"{speaker}: {speech}\n"

    # Extract Answers
    answers_map = {}
    ans_panel_match = re.search(r'<div class="panel answers">(.*?)</div>\s*</div>', content, re.DOTALL)
    if ans_panel_match:
        ans_block = ans_panel_match.group(1)
        ans_lines = re.findall(r'<div>(.*?)</div>', ans_block)
        for line in ans_lines:
            line_text = clean_text(line)
            # Match (1) or （１）
            match = re.match(r'[（\(](\d+)[）\)]\s*(.*)', line_text)
            if match:
                answers_map[match.group(1)] = match.group(2)

    # Extract Exercises and Vocab
    exercises = []
    vocab_list = []
    
    # Regex to capture each q-item block
    # Using a non-greedy match that stops at the next <li class="q-item"> or </ul>
    # This is tricky with regex. Splitting by class="q-item" is safer.
    q_items_split = content.split('class="q-item"')
    # First split is before the first item, skip it.
    
    for i in range(1, len(q_items_split)):
        item = q_items_split[i]
        # Truncate at </li> to avoid capturing too much
        if '</li>' in item:
            item = item.split('</li>')[0]
            
        # q-head
        head_match = re.search(r'class="q-head"[^>]*>(.*?)</div>', item)
        if not head_match: 
            # Try without class attr details
            head_match = re.search(r'<div class="q-head">(.*?)</div>', item)
        
        if not head_match: continue
        
        q_num_text = clean_text(head_match.group(1))
        q_num_match = re.search(r'(\d+)', q_num_text)
        q_num = q_num_match.group(1) if q_num_match else "0"
        
        # hint
        hint_match = re.search(r'class="hint"[^>]*>(.*?)</div>', item)
        hint = clean_text(hint_match.group(1)).replace('【Situación】', '').strip() if hint_match else ""
        
        # q-es
        es_match = re.search(r'class="q-es"[^>]*>(.*?)</div>', item)
        q_es = clean_text(es_match.group(1)).replace('Dices en español:', '').replace('「', '').replace('」', '').strip() if es_match else ""
        
        correct_answer = answers_map.get(q_num, "")
        if not correct_answer:
            correct_answer = "Respuesta no encontrada" # Fallback
        
        exercises.append({
            "type": "comprehension",
            "question": f"{hint}<br><strong>{q_es}</strong>",
            "options": [
                {"text": correct_answer, "correct": True}
            ]
        })
        
        # Populate vocab
        # Use Japanese text as 'kanji'
        # Since we don't have separate kana, use the same text for 'kana' so games don't break
        vocab_list.append({
            "kanji": correct_answer,
            "kana": correct_answer, # Fallback: use the full text as reading
            "romaji": "",
            "es": q_es,
            "audioText": correct_answer,
            "explanation": hint,
            "examples": []
        })

    # Add distractors
    all_answers = [v['kanji'] for v in vocab_list if v['kanji'] != "Respuesta no encontrada"]
    for ex in exercises:
        correct = ex['options'][0]['text']
        if correct == "Respuesta no encontrada":
            continue
            
        import random
        distractors = [a for a in all_answers if a != correct]
        distractors = list(set(distractors))
        
        chosen = []
        if len(distractors) >= 2:
            chosen = random.sample(distractors, 2)
        elif len(distractors) == 1:
            chosen = distractors
        else:
            chosen = ["(Otra respuesta)"]
            
        for c in chosen:
            ex['options'].append({"text": c, "correct": False})
        random.shuffle(ex['options'])

    lesson_obj = {
        "id": f"L{lesson_num}",
        "title": f"Lección {lesson_num}: {title.replace('Situación：', '').strip()}",
        "goals": [
            f"Tema: {topics}",
            "Practicar diálogos situacionales",
            "Aprender expresiones clave"
        ],
        "vocabulary": vocab_list,
        "phrases": [
            {
                "jp_furigana": d['jp'],
                "jp": d['jp'],
                "romaji": "",
                "es": d['speaker'],
                "audioText": d['jp']
            } for d in dialogues
        ],
        "reading": {
            "jp_furigana": full_reading_text.replace('\n', '<br>'),
            "jp": full_reading_text,
            "es": "Lee los diálogos anteriores para practicar.",
            "audioText": full_reading_text.replace('\n', '。')
        },
        "grammarNotes": [
            {
                "title": "Notas de la lección",
                "body": "Revisa las situaciones y cómo responder adecuadamente en cada contexto."
            }
        ],
        "exercises": exercises
    }
    
    lessons_data.append(lesson_obj)

# Read HTML file
html_path = os.path.join(root_dir, "juego_interactivo.html")
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. Update courseData
new_js_data = "const courseData = " + json.dumps({"lessons": lessons_data}, ensure_ascii=False, indent=4) + ";"

# Replace carefully
html_content = re.sub(
    r'const courseData = \{[\s\S]*?\}\s*;\s*(?=\/\/\s*={10,})', 
    new_js_data + "\n\n", 
    html_content
)
# Also fallback replace if the comment marker isn't there (it should be though)

# 2. Update Lesson Select Options
# Clear existing options first to avoid duplicates if running multiple times?
# The regex replaced the whole block <select...>...</select> last time.
new_options = ""
for lesson in lessons_data:
    new_options += f'                <option value="{lesson["id"]}">{lesson["title"]}</option>\n'

select_pattern = r'(<select id="lesson-select"[^>]*>)([\s\S]*?)(</select>)'
html_content = re.sub(select_pattern, f'\\1\n{new_options}            \\3', html_content)

# 3. Update initial lesson ID
# It was likely set to L45 or L1 previously.
# We want L4.
first_lesson_id = lessons_data[0]['id'] if lessons_data else "L4"
# Replace any existing initialization
html_content = re.sub(r'let currentLesson = "[^"]+";', f'let currentLesson = "{first_lesson_id}";', html_content)

# Write output
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully updated {html_path} with correct lesson IDs")
