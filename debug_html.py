import re
import json
import os

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

if not os.path.exists(file_path):
    print("File not found")
    exit()

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} bytes")

# Extract courseData
match = re.search(r'const courseData = (\{[\s\S]*?\});', content)
if match:
    json_str = match.group(1)
    print("Found courseData object.")
    try:
        data = json.loads(json_str)
        print("JSON is valid.")
        print(f"Number of lessons: {len(data.get('lessons', []))}")
        if data.get('lessons'):
            print(f"First lesson ID: {data['lessons'][0]['id']}")
            print(f"First lesson Title: {data['lessons'][0]['title']}")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print("Snippet around error:")
        print(json_str[max(0, e.pos-50):min(len(json_str), e.pos+50)])
else:
    print("Could not find courseData variable using regex.")
    # Print the area where it should be (around script tag)
    script_idx = content.find('<script>')
    if script_idx != -1:
        print("Script tag content start:")
        print(content[script_idx:script_idx+500])

# Check currentLesson initialization
match_lesson = re.search(r'let currentLesson = "(.*?)";', content)
if match_lesson:
    print(f"currentLesson initialized to: {match_lesson.group(1)}")
else:
    print("Could not find currentLesson initialization")
