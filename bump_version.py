import re

def bump_version():
    path = "templates/dashboard.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(r'v1\.1\.85', 'v1.1.86', content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Bumped version to 1.1.86")

if __name__ == "__main__":
    bump_version()
