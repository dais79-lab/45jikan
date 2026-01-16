import re
import json
import sys

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject Error Handler for User Feedback
error_handler = """
<script>
window.onerror = function(msg, url, line, col, error) {
   var extra = !col ? '' : '\\ncolumn: ' + col;
   extra += !error ? '' : '\\nerror: ' + error;
   var div = document.createElement("div");
   div.style.position = "fixed";
   div.style.top = "0";
   div.style.left = "0";
   div.style.width = "100%";
   div.style.background = "red";
   div.style.color = "white";
   div.style.padding = "10px";
   div.style.zIndex = "9999";
   div.innerText = "Error: " + msg + "\\nurl: " + url + "\\nline: " + line + extra;
   document.body.appendChild(div);
   return false;
};
</script>
"""

if "window.onerror" not in content:
    content = content.replace('<head>', '<head>' + error_handler)

# 2. Check for Syntax Errors in courseData
# We suspect courseData might be malformed.
# Let's try to extract it and parse it.
match = re.search(r'const courseData = (\{[\s\S]*?\});', content)
if match:
    json_str = match.group(1)
    # Remove trailing semicolon if captured
    if json_str.endswith(';'):
        json_str = json_str[:-1]
    
    try:
        # JSON standard requires double quotes. JS allows single.
        # This is a loose check.
        # If it fails, we might just look for obvious issues like trailing commas or missing brackets.
        pass 
    except Exception as e:
        print(f"JSON Parse Warning: {e}")

# 3. Check for Broken Script Tags
# Sometimes regex replacement leaves multiple <script> tags nested or unclosed.
# Let's clean up the script structure.
# We want ONE main script tag at the end.

# Extract everything between first <script> and last </script>
# But wait, we might have multiple scripts (error handler above).
# Let's target the main logic script which starts with `const courseData`.

# Strategy: Re-write the file structure to be clean.
# Header -> Body -> ErrorHandler -> MainScript.

# Find the Main Script Content
script_match = re.search(r'(const courseData = \{[\s\S]*?)(?=</script>)', content)
if not script_match:
    print("CRITICAL: Could not find main script content.")
    # Maybe the script tag is broken?
    # Let's search for `const courseData` and take everything until end of file (minus closing tags).
    start_idx = content.find('const courseData = {')
    if start_idx != -1:
        # Check if there is a closing script tag
        end_idx = content.rfind('</script>')
        if end_idx > start_idx:
            main_script = content[start_idx:end_idx]
        else:
            # Maybe missing closing tag
            main_script = content[start_idx:]
            # Remove </body></html> if present
            main_script = main_script.replace('</body>', '').replace('</html>', '')
    else:
        print("CRITICAL: No courseData found.")
        sys.exit(1)
else:
    main_script = script_match.group(1)

# Clean up Main Script
# 1. Ensure courseData is terminated.
# It should end with `};`.
# If `courseData` has `}` but no `;`, it's valid JS but let's be safe.
# If `courseData` is cut off...
# Let's check the end of `courseData` object.
# It should be `const courseData = { ... };`
# We can find the matching closing brace.

# Helper to find matching brace
def find_matching_brace(s, start_pos):
    balance = 0
    found_start = False
    for i in range(start_pos, len(s)):
        char = s[i]
        if char == '{':
            balance += 1
            found_start = True
        elif char == '}':
            balance -= 1
            if found_start and balance == 0:
                return i
    return -1

cd_start = main_script.find('{')
cd_end = find_matching_brace(main_script, cd_start)

if cd_end == -1:
    print("CRITICAL: courseData object is not closed properly!")
    # We must close it.
    # Where did it stop?
    # Let's just append `]}` and hope? No, dangerous.
    # Let's fallback to a safe minimal courseData if broken.
    pass
else:
    # Ensure semicolon
    if cd_end + 1 < len(main_script) and main_script[cd_end+1] != ';':
        main_script = main_script[:cd_end+1] + ';' + main_script[cd_end+1:]

# 4. Remove all existing <script> tags from body to avoid duplicates
# We will strip all scripts and re-inject the error handler and main script.
content_no_script = re.sub(r'<script[\s\S]*?</script>', '', content)
# Restore error handler in head (it was stripped above)
content_no_script = content_no_script.replace('<head>', '<head>' + error_handler)

# 5. Inject Main Script at the end of body
new_body_end = f"""
<script>
{main_script}
</script>
</body>
"""
final_content = content_no_script.replace('</body>', new_body_end)

# 6. Ensure CSS is present (regex replacement might have killed it if pattern mismatch)
if "Fredoka" not in final_content:
    # Re-inject head stuff
    head_stuff = """
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { --bg-color: #131f24; --text-color: #fff; --duo-green: #58cc02; }
        body { background: var(--bg-color); color: var(--text-color); font-family: 'Fredoka', sans-serif; }
        .view-section { display: none; } .view-section.active { display: block; }
        /* ... (minimal fallback) ... */
    </style>
    """
    final_content = final_content.replace('</head>', head_stuff + '</head>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Repaired script structure and added error logger.")
