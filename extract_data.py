import os
import re
import json
from bs4 import BeautifulSoup

# Define the directory
root_dir = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15"

# List of files to process
files = [f"45jikan{i}kac.html" for i in range(4, 16)]
lessons_data = []

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

for filename in files:
    file_path = os.path.join(root_dir, filename)
    if not os.path.exists(file_path):
        print(f"File not found: {filename}")
        continue
        
    print(f"Processing {filename}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    # Extract Lesson Number
    lesson_num = re.search(r'(\d+)', filename).group(1)
    
    # Extract Title
    title_el = soup.find('div', class_='title')
    title = clean_text(title_el.text) if title_el else f"Lección {lesson_num}"
    
    # Extract Subtitle/Badge (Topics)
    badge_el = soup.find('div', class_='badge')
    topics = clean_text(badge_el.text) if badge_el else ""
    
    # Extract Dialogues (Phrases/Reading)
    dialogues = []
    dialog_divs = soup.find_all('div', class_='dialog')
    full_reading_text = ""
    
    for d in dialog_divs:
        # Each dialog has names and text. 
        # Structure: <div class="name">Name:</div><div>Text</div>
        # We need to pair them.
        names = d.find_all('div', class_='name')
        # The text following the name is the next sibling div usually, or just text node?
        # Looking at previous file reads:
        # <div class="name">おの:</div><div>リーさん、かぞくは なんにんですか。</div>
        
        # BeautifulSoup treats them as siblings.
        # Let's iterate through children.
        current_speaker = ""
        for child in d.children:
            if child.name == 'div' and 'name' in child.get('class', []):
                current_speaker = clean_text(child.text).replace(':', '')
            elif child.name == 'div':
                text = clean_text(child.text)
                if text:
                    dialogues.append({
                        "speaker": current_speaker,
                        "jp": text,
                        # We don't have romaji or es translation for dialogues in the source, 
                        # except maybe implicitly in the Q&A later?
                        # We'll leave them blank or try to infer.
                        # Actually, looking at the file structure, there is no direct translation for the dialogues.
                        "romaji": "", 
                        "es": "" 
                    })
                    full_reading_text += f"{current_speaker}: {text}\n"

    # Extract Answers first to map them to questions
    answers_map = {}
    answers_panel = soup.find('div', class_='panel answers')
    if answers_panel:
        answer_lines = answers_panel.find_all('div')
        for line in answer_lines:
            text = clean_text(line.text)
            # Format: （１） わたしの かぞくは 5人です。
            match = re.match(r'[（\(](\d+)[）\)]\s*(.*)', text)
            if match:
                q_num = match.group(1)
                ans_text = match.group(2)
                answers_map[q_num] = ans_text

    # Extract Exercises (Situación y Pregunta)
    exercises = []
    q_items = soup.find_all('li', class_='q-item')
    
    vocab_list = [] # We will use these as "Flashcards"
    
    for item in q_items:
        q_head = item.find('div', class_='q-head')
        if not q_head: continue
        
        q_num_text = clean_text(q_head.text)
        q_num_match = re.search(r'(\d+)', q_num_text)
        q_num = q_num_match.group(1) if q_num_match else "0"
        
        hint_el = item.find('div', class_='hint')
        hint = clean_text(hint_el.text).replace('【Situación】', '').strip() if hint_el else ""
        
        q_es_el = item.find('div', class_='q-es')
        q_es = clean_text(q_es_el.text).replace('Dices en español:', '').replace('「', '').replace('」', '').strip() if q_es_el else ""
        
        correct_answer = answers_map.get(q_num, "")
        
        # Create Exercise
        exercises.append({
            "type": "comprehension", # Using comprehension style for Q&A
            "question": f"{hint}<br><strong>{q_es}</strong>",
            "options": [
                {"text": correct_answer, "correct": True},
                {"text": "(Respuesta incorrecta aleatoria)", "correct": False} # We might need to generate distractors
            ]
        })
        
        # Add to vocab/flashcards (Front: Spanish/Situation, Back: Japanese Answer)
        if correct_answer:
            vocab_list.append({
                "kanji": correct_answer, # The Japanese answer
                "kana": "", # We assume the text is mixed kana/kanji. We don't have pure kana.
                "romaji": "", # We don't have romaji
                "es": q_es, # The Spanish prompt
                "audioText": correct_answer,
                "explanation": hint,
                "examples": []
            })

    # Since we don't have distractors for exercises, we can grab answers from other questions in the same lesson
    all_answers = [v['kanji'] for v in vocab_list]
    for ex in exercises:
        correct = ex['options'][0]['text']
        # Pick 2 random wrong answers
        import random
        distractors = [a for a in all_answers if a != correct]
        if len(distractors) >= 2:
            chosen = random.sample(distractors, 2)
        elif len(distractors) == 1:
            chosen = distractors
        else:
            chosen = ["(Otra respuesta)"]
            
        ex['options'] = [{"text": correct, "correct": True}]
        for c in chosen:
            ex['options'].append({"text": c, "correct": False})
        random.shuffle(ex['options'])

    # Structure for courseData
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
                "jp_furigana": d['jp'], # We don't have real furigana, just using plain text
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

# Output JSON
output_json = json.dumps({"lessons": lessons_data}, ensure_ascii=False, indent=2)
with open(os.path.join(root_dir, 'extracted_data.json'), 'w', encoding='utf-8') as f:
    f.write(output_json)

print("Data extraction complete.")
