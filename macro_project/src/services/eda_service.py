from pathlib import Path
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns

class EDAService:
    """Generate and save EDA outputs for the indexed image dataset."""
    def __init__(self, dataframe: pd.DataFrame, output_dir: Path) -> None:
        self.dataframe : pd.DataFrame = dataframe         
        self.output_dir = output_dir
    def save_class_distribution(self) -> None:         
        """Save a class-count chart for the dataset."""
        plt.figure(figsize=(12, 6))         
        order = self.dataframe["label"].value_counts().index         
        sns.countplot(data=self.dataframe, x="label", order=order)         
        plt.xticks(rotation=90)         
        plt.title("Macroinvertebrate Images per Class")         
        plt.tight_layout()         
        plt.savefig(self.output_dir / "class_distribution.png")         
        plt.close()
    def save_image_size_distribution(self) -> None:         
        """Save width and height distribution charts."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))         
        sns.histplot(self.dataframe["width"], bins=20, ax=axes[0])         
        sns.histplot(self.dataframe["height"], bins=20, ax=axes[1])         
        axes[0].set_title("Image Width Distribution")         
        axes[1].set_title("Image Height Distribution")         
        plt.tight_layout()         
        plt.savefig(self.output_dir / "image_size_distribution.png")         
        plt.close()
    def build_summary(self) -> dict[str, float]:         
        """Return key dataset summary statistics."""
        return {
            "total_images": int(len(self.dataframe)),
            "total_classes": int(self.dataframe["label"].nunique()),
            "mean_width": float(self.dataframe["width"].mean()),
            "mean_height": float(self.dataframe["height"].mean()),         }
