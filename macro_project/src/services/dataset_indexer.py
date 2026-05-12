from pathlib import Path
import cv2
import pandas as pd

from config import RAW_DATA_DIR, SUPPORTED_EXTENSIONS

def do_nothing(*args, **kwargs):
    pass

class DatasetIndexer:
    """Scan the dataset folder and build a tabular image index."""
    def __init__(self, data_dir: Path = RAW_DATA_DIR) -> None:
        self.data_dir = data_dir
        self.counter :int = 0
        self.output: pd.DataFrame | None = None
    def build_dataframe(self, func = do_nothing, final = do_nothing) -> pd.DataFrame:
        """Return one row per image with file path, label, and dimensions."""
        records = []

        for file_path in self.data_dir.rglob("*"):
            func()
            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            
            image = cv2.imread(str(file_path))
            if image is None:
                continue
            
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            label = file_path.parent.name
            
            records.append(
                {
                    "file_path": str(file_path),
                    "label": label,
                    "width": width,
                    "height": height,
                    "channels": channels,
                }
            )
            self.counter = len(records)
        final()
        self.output = pd.DataFrame(records)
        return self.output