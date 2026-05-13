from pathlib import Path
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns

class EDAService:
    """Generate and save EDA outputs for the indexed image dataset."""
    def __init__(self, dataframe: pd.DataFrame, output_dir: Path) -> None:
        self.base_dataframe : pd.DataFrame = dataframe         
        self.output_dir = output_dir
        print(output_dir)
        self.filterd_dataframe: pd.DataFrame = dataframe
    
    def filter_data_frame(self, labels:list[str]):
        self.filterd_dataframe = self.base_dataframe.copy().filter(items=labels)

    def save_class_distribution(self) -> Path:         
        """Save a class-count chart for the dataset."""
        plt.figure(figsize=(12, 6))         
        order = self.filterd_dataframe["label"].value_counts().index         
        sns.countplot(data=self.filterd_dataframe, x="label", order=order)         
        plt.xticks(rotation=90)         
        plt.title("Macroinvertebrate Images per Class")         
        plt.tight_layout()
        output_file_name = self.output_dir / "class_distribution.png"
        plt.savefig(output_file_name)         
        plt.close()
        return output_file_name
    def save_image_size_distribution(self) -> Path:         
        """Save width and height distribution charts."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))         
        sns.histplot(self.filterd_dataframe["width"], bins=20, ax=axes[0]) #type: ignore    
        sns.histplot(self.filterd_dataframe["height"], bins=20, ax=axes[1]) #type: ignore     
        axes[0].set_title("Image Width Distribution")         
        axes[1].set_title("Image Height Distribution")         
        plt.tight_layout()   
        output_file_name = self.output_dir / "image_size_distribution.png"
        plt.savefig(output_file_name)         
        plt.close()
        return output_file_name
    def build_summary(self) -> dict[str, float]:         
        """Return key dataset summary statistics."""
        return {
            "total_images": int(len(self.filterd_dataframe)),
            "total_classes": int(self.filterd_dataframe["label"].nunique()),
            "mean_width": float(self.filterd_dataframe["width"].mean()),
            "mean_height": float(self.filterd_dataframe["height"].mean()),}
