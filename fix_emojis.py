import os

for root, dirs, files in os.walk("app"):
    for file in files:
        if file.endswith((".html", ".js", ".py", ".css")):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # fix the broken man teacher emoji
            new_content = content.replace('👨\u200d<i class="fa-solid fa-school"></i>', '<i class="fa-solid fa-chalkboard-user"></i>')
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed {path}")
