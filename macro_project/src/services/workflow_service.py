from pathlib import Path

import joblib
import pandas as pd

from src.config import EDA_OUTPUT_DIR, MODEL_OUTPUT_DIR
from src.services.dataset_indexer import DatasetIndexer
from src.services.eda_service import EDAService

class WorkflowService:
    """Coordinate the shared workflow used by batch, GUI, and console entry points."""

    def __init__(self) -> None:
        EDA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        self.indexer = DatasetIndexer()
        self.dataframe: pd.DataFrame | None = None

    def load_dataframe(self) -> pd.DataFrame:
        """Load and cache the indexed dataset."""

        if self.dataframe is None:
            self.dataframe = self.indexer.build_dataframe()
        return self.dataframe
    
    def show_summary(self) -> dict[str, float]:
        """Build and print dataset summary statistics."""

        dataframe = self.load_dataframe()
        eda = EDAService(dataframe, EDA_OUTPUT_DIR)
        summary = eda.build_summary()
        print(summary)
        return summary
    
    def generate_eda(self, labels:list[str]|None = None) -> None:
        """Create and save the main EDA outputs."""
            
        dataframe = self.load_dataframe()
        eda = EDAService(dataframe, EDA_OUTPUT_DIR)
        eda.save_class_distribution()
        eda.save_image_size_distribution()

    def run_full_pipeline(self) -> None:
        """Run the default Stage 1 workflow."""

        self.show_summary()
        self.generate_eda()
