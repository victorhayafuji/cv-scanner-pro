import os
import shutil
from pathlib import Path

# Configuration
SOURCE_DIRS = [
    Path("src"),
    Path("frontend/src"),
    Path("."),  # Root for main.py etc.
]
TARGET_DIR = Path("txt-files")
EXTENSIONS = {".py", ".jsx", ".js", ".css", ".md", ".html"}
IGNORE_DIRS = {"node_modules", ".venv", "__pycache__", ".git", "dist", "coverage"}
IGNORE_FILES = {"package-lock.json", "yarn.lock"}

def should_process(file_path: Path) -> bool:
    if file_path.name in IGNORE_FILES:
        return False
    # Check if any parent part is in IGNORE_DIRS
    for part in file_path.parts:
        if part in IGNORE_DIRS:
            return False
    return file_path.suffix in EXTENSIONS

def get_target_path(source_file: Path, target_dir: Path) -> Path:
    """
    Determines the target path.
    1. Checks if 'stem.txt' exists (legacy mapping).
    2. Defaults to 'filename.txt'.
    """
    legacy_name = target_dir / f"{source_file.stem}.txt"
    if legacy_name.exists():
        return legacy_name
    
    # New convention: preserve extension for clarity (e.g., App.jsx.txt)
    return target_dir / f"{source_file.name}.txt"

def sync_files():
    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True)
        print(f"Created directory: {TARGET_DIR}")

    count = 0
    updated = 0
    
    for src_dir in SOURCE_DIRS:
        if not src_dir.exists():
            continue
            
        # Handle root specially to avoid recursive walk into all ignore dirs
        if src_dir == Path("."):
            iterator = (p for p in src_dir.iterdir() if p.is_file())
        else:
            iterator = src_dir.rglob("*")

        for file_path in iterator:
            if not file_path.is_file():
                continue
            
            if not should_process(file_path):
                continue

            target_path = get_target_path(file_path, TARGET_DIR)
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # Add header for context
                header = f"# Source: {file_path.as_posix()}\n# Timestamp: {os.path.getmtime(file_path)}\n\n"
                full_content = header + content
                
                # Write if changed or new
                if not target_path.exists() or target_path.read_text(encoding='utf-8', errors='ignore') != full_content:
                    target_path.write_text(full_content, encoding='utf-8')
                    updated += 1
                
                count += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    print(f"Processed {count} files.")
    print(f"Updated/Created {updated} files in {TARGET_DIR}")

if __name__ == "__main__":
    sync_files()
