import re

file_path = r"c:\Users\etc}\Desktop\45jikan imagenesL4-L15\45jikan imagenesL4-L15\juego_interactivo.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the broken "jp" field in "reading" object
# It looks like: "jp": "Start...
# ...
# End",
# We want to replace the physical newlines with \n literal

def fix_newlines(match):
    full_str = match.group(0)
    # Replace real newlines with \n literal
    # But be careful not to replace newlines that are outside the string (formatting)
    # The regex captures the whole key-value pair.
    # We only want to touch the value content.
    
    # Actually, simpler approach:
    # content is the whole match: "jp": "Line1\nLine2\nLine3",
    # We want "jp": "Line1\nLine2\nLine3", (where \n is literal)
    
    # Let's extract the value part
    prefix = '"jp": "'
    suffix = '",'
    
    if full_str.startswith(prefix) and full_str.endswith(suffix):
        inner = full_str[len(prefix):-len(suffix)]
        # Replace newlines with \n
        fixed_inner = inner.replace('\n', '\\n').replace('\r', '')
        return prefix + fixed_inner + suffix
    return full_str

# Regex matches "jp": "..." where ... can contain newlines
# We look for "jp": " followed by non-quote chars or newlines, ending with ",
pattern = r'"jp": "((?:[^"]|\n)*?)(?<!\\)",'

# Wait, checking for unescaped quote might be tricky if the text contains quotes.
# But JSON strings escape quotes. So we look for ", that is not preceded by \
# The text seems simple enough.

# Let's try to match specifically the reading section "jp" field.
# It seems to be indented.
# Pattern: `^\s*"jp": "[\s\S]*?",$` multiline?

# Refined pattern:
# Look for "jp": " start
# Match anything until ",
# But since it's broken JSON, the next line is not indented correctly or whatever.
# Actually the file read shows:
# 809->                "jp": "おの: ...
# 810->リー: ...
# ...
# 822->",

# So it spans lines.
# We will use re.sub with a callback.

content_fixed = re.sub(r'"jp": "([\s\S]*?)(?<!\\)",', lambda m: m.group(0).replace('\n', '\\n').replace('\r', ''), content)

# Check if it worked by printing a snippet? No, just write it.
# Also check for "audioText" which might have same issue?
# Line 824: "audioText": "..." seems on one line.
# Line 780: "jp": "..." seems on one line (for phrases).
# It seems only the "reading" section's "jp" field is affected because it's a long dialogue.

# Wait, `content_fixed` will replace ALL "jp" fields.
# Phrases also have "jp".
# If phrases are on one line, `replace('\n', '\\n')` does nothing.
# So it's safe.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_fixed)

print("Fixed newlines in JSON strings.")
