from pathlib import Path

def ensure_directory(folder_path: str|Path) -> Path:
    """ensures there is a current directory"""

    directory = Path(folder_path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory