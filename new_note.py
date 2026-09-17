import sys
import os
import re
from datetime import date

# Ensure utf-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "problem-template.md")
PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), "problems")


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text

def main():
    print("=== 🚀 LeetCode New Note Generator ===")
    
    if len(sys.argv) >= 3:
        problem_id = sys.argv[1].strip()
        title = sys.argv[2].strip()
        difficulty = sys.argv[3].strip() if len(sys.argv) > 3 else "Medium"
        topic = sys.argv[4].strip() if len(sys.argv) > 4 else "Array / Hash Table"
    else:
        problem_id = input("1. Problem Number (e.g. 242): ").strip()
        title = input("2. Problem Title (e.g. Valid Anagram): ").strip()
        difficulty = input("3. Difficulty (Easy/Medium/Hard) [Easy]: ").strip() or "Easy"
        topic = input("4. Topic / Pattern [Array / Hash Table]: ").strip() or "Array / Hash Table"

    if not problem_id or not title:
        print("❌ Error: Problem Number and Title are required.")
        return

    # Pad problem ID to 4 digits: e.g. 1 -> 0001, 242 -> 0242
    padded_id = problem_id.zfill(4)
    slug = slugify(title)
    filename = f"{padded_id}-{slug}.md"
    target_path = os.path.join(PROBLEMS_DIR, filename)

    if os.path.exists(target_path):
        print(f"⚠️ Warning: Note already exists at: {target_path}")
        overwrite = input("Overwrite? (y/N): ").strip().lower()
        if overwrite != "y":
            print("Cancelled.")
            return

    # Read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Fill placeholders
    today = date.today().strftime("%Y-%m-%d")
    leetcode_url = f"https://leetcode.com/problems/{slug}/"
    
    content = content.replace("# [ID. Problem Name]", f"# {padded_id}. {title}")
    content = content.replace("[LeetCode URL](https://leetcode.com/problems/...)", leetcode_url)
    content = content.replace("`Easy` | `Medium` | `Hard`", f"`{difficulty}`")
    content = content.replace("`Array` / `Hash Table` / `Two Pointers` / `Sliding Window` / ...", f"`{topic}`")
    content = content.replace("YYYY-MM-DD", today)

    os.makedirs(PROBLEMS_DIR, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created: problems/{filename}")
    print(f"👉 Link to problem: {leetcode_url}")
    print("\nNext steps:")
    print(f"1. Open 'problems/{filename}' and write your solution & takeaways.")
    print("2. Add an entry to 'README.md' and '_sidebar.md'.")

if __name__ == "__main__":
    main()
