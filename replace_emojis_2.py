import os

replacements = {
    "✏️": '<i class="fa-solid fa-pen"></i>',
    "✉️": '<i class="fa-solid fa-envelope"></i>',
    "⚙️": '<i class="fa-solid fa-gear"></i>',
    "⚠️": '<i class="fa-solid fa-triangle-exclamation"></i>',
    "➕": '<i class="fa-solid fa-plus"></i>',
    "✏": '<i class="fa-solid fa-pen"></i>',
    "✉": '<i class="fa-solid fa-envelope"></i>',
    "⚙": '<i class="fa-solid fa-gear"></i>',
    "⚠": '<i class="fa-solid fa-triangle-exclamation"></i>'
}

for root, dirs, files in os.walk("app"):
    for file in files:
        if file.endswith((".html", ".js", ".py", ".css")):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            for emoji, icon in replacements.items():
                new_content = new_content.replace(emoji, icon)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {path}")
