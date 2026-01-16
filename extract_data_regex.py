import os
import re
import json

# Define the directory
root_dir = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15"

# List of files to process
files = [f"45jikan{i}kac.html" for i in range(4, 16)]
lessons_data = []

def clean_text(text):
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def get_tag_content(tag_name, class_name, html):
    # Very basic regex to find content inside <div class="classname">...</div>
    # This assumes no nested divs with same class, which holds for this simple structure
    pattern = f'<div class="{class_name}"[^>]*>(.*?)</div>'
    return re.findall(pattern, html, re.DOTALL)

for filename in files:
    file_path = os.path.join(root_dir, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        continue
        
    print(f"Processing {filename}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract Lesson Number
    lesson_num = re.search(r'(\d+)', filename).group(1)
    
    # Extract Title
    title_match = re.search(r'<div class="title">(.*?)</div>', content)
    title = clean_text(title_match.group(1)) if title_match else f"Lección {lesson_num}"
    
    # Extract Subtitle/Badge
    badge_match = re.search(r'<div class="badge">(.*?)</div>', content)
    topics = clean_text(badge_match.group(1)) if badge_match else ""
    
    # Extract Dialogues
    # The dialog structure is: <div class="dialog">\s*<div class="name">Name:</div><div>Text</div>...
    # We can split by <div class="dialog"> to get blocks
    dialog_blocks = content.split('<div class="dialog">')[1:]
    
    dialogues = []
    full_reading_text = ""
    
    for block in dialog_blocks:
        # Find the end of the dialog div. It usually ends before the next closing div of the parent panel
        # But easier is to just regex match the name and text lines inside
        # Pattern: <div class="name">(.*?)</div><div>(.*?)</div>
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
    # Look for <div class="panel answers">...</div>
    answers_map = {}
    ans_panel_match = re.search(r'<div class="panel answers">(.*?)</div>\s*</div>', content, re.DOTALL)
    if ans_panel_match:
        ans_block = ans_panel_match.group(1)
        # Find lines like <div>（１）...</div>
        ans_lines = re.findall(r'<div>(.*?)</div>', ans_block)
        for line in ans_lines:
            line_text = clean_text(line)
            match = re.match(r'[（\(](\d+)[）\)]\s*(.*)', line_text)
            if match:
                answers_map[match.group(1)] = match.group(2)

    # Extract Exercises (Situación y Pregunta)
    exercises = []
    vocab_list = []
    
    # Find all <li class="q-item">...</li>
    # Since regex is greedy/tricky with nested tags, and we know the structure:
    q_items = re.findall(r'<li class="q-item">(.*?)</li>', content, re.DOTALL)
    
    for item in q_items:
        # q-head
        head_match = re.search(r'<div class="q-head">(.*?)</div>', item)
        if not head_match: continue
        q_num_text = clean_text(head_match.group(1))
        q_num_match = re.search(r'(\d+)', q_num_text)
        q_num = q_num_match.group(1) if q_num_match else "0"
        
        # hint
        hint_match = re.search(r'<div class="hint">(.*?)</div>', item)
        hint = clean_text(hint_match.group(1)).replace('【Situación】', '').strip() if hint_match else ""
        
        # q-es
        es_match = re.search(r'<div class="q-es">(.*?)</div>', item)
        q_es = clean_text(es_match.group(1)).replace('Dices en español:', '').replace('「', '').replace('」', '').strip() if es_match else ""
        
        correct_answer = answers_map.get(q_num, "")
        
        exercises.append({
            "type": "comprehension",
            "question": f"{hint}<br><strong>{q_es}</strong>",
            "options": [
                {"text": correct_answer, "correct": True}
            ]
        })
        
        if correct_answer:
            vocab_list.append({
                "kanji": correct_answer,
                "kana": "",
                "romaji": "",
                "es": q_es,
                "audioText": correct_answer,
                "explanation": hint,
                "examples": []
            })

    # Add distractors
    all_answers = [v['kanji'] for v in vocab_list]
    for ex in exercises:
        correct = ex['options'][0]['text']
        import random
        distractors = [a for a in all_answers if a != correct]
        # remove duplicates from distractors
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
                "es": "Diálogo: " + d['speaker'],
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

output_json = json.dumps({"lessons": lessons_data}, ensure_ascii=False, indent=2)
with open(os.path.join(root_dir, 'extracted_data.json'), 'w', encoding='utf-8') as f:
    f.write(output_json)

print("Data extraction complete.")
