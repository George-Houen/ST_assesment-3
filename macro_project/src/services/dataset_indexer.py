from pathlib import Path
import cv2
import pandas as pd

from config import RAW_DATA_DIR, SUPPORTED_EXTENSIONS

class DatasetIndexer:
    """Scan the dataset folder and build a tabular image index."""
    def __init__(self, data_dir: Path = RAW_DATA_DIR) -> None:
        self.data_dir = data_dir
        self.counter :int = 0
        self.output: pd.DataFrame | None = None
    def build_dataframe(self, func = None, final = None) -> pd.DataFrame:
        """Return one row per image with file path, label, and dimensions."""
        records = []

        for file_path in self.data_dir.rglob("*"):
            if func: func()
            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            
            image = cv2.imread(str(file_path))
            if image is None:
                records.append(
                    {
                        "file_path": str(file_path),
                        "label": file_path.parent.name,
                        "readable": image is not None,
                    }
                )
                continue
            
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            label = file_path.parent.name
            extension = file_path.suffix.lower()
            if height > 0:
                aspect_ratio = width/height
            else:
                aspect_ratio = 0
            
            records.append(
                {
                    "file_path": str(file_path),
                    "label": label,
                    "width": width,
                    "height": height,
                    "channels": channels,
                    "readable": True,
                    "file_extension": extension,
                    "aspect_ratio" : aspect_ratio
                }
            )
            self.counter = len(records)
        if final:final()
        self.output = pd.DataFrame(records)
        return self.output