from pathlib import Path

def ensure_directory(folder_path: str|Path) -> Path:
    directory = Path(folder_path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory