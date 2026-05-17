
"""
*******************************
Author:
u3324971 u3334568 
Assessment 3 
part 1
17/ 05/2026
Programming:
*******************************
"""

from pathlib import Path

def ensure_directory(folder_path: str|Path) -> Path:
    """ensures there is a current directory"""

    directory = Path(folder_path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory