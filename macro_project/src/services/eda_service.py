from pathlib import Path

import matplotlib
matplotlib.use("Agg")# DO NOT TOUCH: this has to default to a diffirent thread so that it doesnt mess with the GUI

import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns
import numpy as np
import cv2
from typing import Callable, Any

from config import (
    CLASS_IMBALANCE_REPORT_PATH,
    PIXEL_ANALYSIS_SAMPLE_SIZE,
    QUALITY_ISSUES_PATH,
    SAMPLE_GRID_MAX_IMAGES,
    STAGE2_RECOMMENDATIONS_PATH,
    UNUSUAL_ASPECT_RATIO_HIGH,
    UNUSUAL_ASPECT_RATIO_LOW,
    VERY_SMALL_IMAGE_THRESHOLD,
)

from utils.file_utils import ensure_directory

class EDAService:
    """Generate and save EDA outputs for the indexed image dataset."""
    def __init__(self, dataframe: pd.DataFrame, output_dir_eda: Path, output_dir_report: Path) -> None:
        self.base_dataframe : pd.DataFrame = dataframe         
        self.output_dir_eda : Path = output_dir_eda
        self.output_dir_report: Path = output_dir_report
        self.filterd_dataframe: pd.DataFrame = dataframe
        readable_mask  = self.base_dataframe["readable"].astype(bool)
        self.readable_dataframe = self.base_dataframe[readable_mask]

        ensure_directory(self.output_dir_eda)
        ensure_directory(self.output_dir_report)

        self.output_summery: dict[str, int | float | str] = {}
        self.output_images:dict[str, Path] = {}
        self.track_save_all_progress : str = ""
    
    def filter_data_frame(self, labels:list[str]):
        print(labels)
        self.filterd_dataframe = self.base_dataframe[self.base_dataframe["label"].isin(labels)] #type:ignore
        readable_mask = self.base_dataframe["readable"].astype(bool)
        self.readable_dataframe = self.filterd_dataframe[readable_mask]
    
    def save_all(self, func_each : Callable[[], Any] | None = None, func_end: Callable[[],Any] | None = None) -> dict[str, Path]:
        operations = {
            "class_distribution" : self.save_class_distribution,
            "image_size_distribution" : self.save_image_size_distribution,
            "width_height_scatter_plot" : self.save_width_height_scatter_plot,
            "sample_image_grid" : self.save_sample_image_grid,
            "height_by_class_boxplot" : self.save_height_by_class_boxplot,
            #"pixel_intensity_histogram" : self.save_pixel_intensity_histogram,
        }
        output: dict[str, Path] = {}
        for title, func in operations.items():
            self.track_save_all_progress = title
            if func_each is not None:
                func_each()
            output[title]=func()
        self.output_images = output
        if func_end:func_end()
        self.save_stage2_recommendations()
        self.save_image_quality_issues()
        self.save_class_imbalance_report()
        return output
    
    def build_summary(self) -> dict[str, int | float | str]:         
        """Return key dataset summary statistics."""

        readable = self._require_readable_images()
        output : dict[str, int | float | str] = {
            "total_images": self._safe_int(len(readable)),
            "total_classes": self._safe_int(readable["label"].nunique()),
            "mean_width": self._safe_round(readable["width"].mean()),
            "mean_height": self._safe_round(readable["height"].mean()),
            "min_width": self._safe_int(readable["width"].min()), #type: ignore
            "max_width": self._safe_int(readable["width"].max()), #type: ignore
            "min_height": self._safe_int(readable["height"].min()), #type: ignore
            "max_height": self._safe_int(readable["height"].max()), #type: ignore
            "number_of_unreadable_files": int((~self.readable_dataframe["readable"]).sum()),
            "supported_file_types_found": str(", ".join(sorted(self.readable_dataframe["file_extension"].unique()))) #type: ignore
            }
        self.output_summery
        return output
    
    def save_class_distribution(self) -> Path:         
        """Save a class-count chart for the dataset."""
        readable = self._require_readable_images()

        plt.figure(figsize=(12, 6)) #type: ignore       
        order = readable["label"].value_counts().index #type: ignore
        sns.countplot(data=readable, x="label", order=order) #type: ignore
        plt.xticks(rotation=90) #type: ignore
        plt.title("Macroinvertebrate Images per Class") #type: ignore
        plt.tight_layout()
        output_file_name : Path = self.output_dir_eda / "class_distribution.png"
        plt.savefig(output_file_name) #type: ignore    
        plt.close()
        return output_file_name
    
    def save_image_size_distribution(self) -> Path:         
        """Save width and height distribution charts."""
        readable = self._require_readable_images()

        fig, axes = plt.subplots(1, 2, figsize=(12, 5)) #type: ignore
        sns.histplot(readable["width"], bins=20, ax=axes[0]) #type: ignore    
        sns.histplot(readable["height"], bins=20, ax=axes[1]) #type: ignore     
        axes[0].set_title("Image Width Distribution")
        axes[1].set_title("Image Height Distribution")
        plt.tight_layout()
        output_file_name = self.output_dir_eda / "image_size_distribution.png"
        plt.savefig(output_file_name) #type: ignore
        plt.close()
        return output_file_name
    


    #following functions provided from Pranav by email with permision:

    def save_width_height_scatter_plot(self) -> Path:
        """Save a scatter plot of image width versus height."""
        readable = self._require_readable_images()
    
        plt.figure(figsize=(8, 6)) #type: ignore
        sns.scatterplot(data=readable, x="width", y="height", hue="label", alpha=0.75)
        plt.title("Image Width Versus Height") #type: ignore
        plt.xlabel("Width in pixels") #type: ignore
        plt.ylabel("Height in pixels") #type: ignore
        plt.legend(title="Class", bbox_to_anchor=(1.05, 1), loc="upper left") #type: ignore
        plt.tight_layout()
    
        output_path = self.output_dir_eda / "width_height_scatter.png"
        plt.savefig(output_path, dpi=150) #type: ignore
        plt.close()
        return output_path

    def save_sample_image_grid(self) -> Path:
        """Save a boxplot comparing image widths by class."""
        readable = self._require_readable_images()
    
        plt.figure(figsize=(11, 6)) #type: ignore
        sns.boxplot(data=readable, x="label", y="width", color="#72B7B2")
        plt.title("Image Width by Class") #type: ignore
        plt.xlabel("Class label") #type: ignore
        plt.ylabel("Width in pixels") #type: ignore
        plt.xticks(rotation=35, ha="right") #type: ignore
        plt.tight_layout()
    
        output_path = self.output_dir_eda / "width_by_class_boxplot.png"
        plt.savefig(output_path, dpi=150) #type: ignore
        plt.close()
        return output_path
    
    def save_height_by_class_boxplot(self) -> Path:
        """Save a boxplot comparing image heights by class."""
        readable = self._require_readable_images()
    
        plt.figure(figsize=(11, 6)) #type: ignore
        sns.boxplot(data=readable, x="label", y="height", color="#54A24B")
        plt.title("Image Height by Class") #type: ignore
        plt.xlabel("Class label") #type: ignore
        plt.ylabel("Height in pixels") #type: ignore
        plt.xticks(rotation=35, ha="right") #type: ignore
        plt.tight_layout()
    
        output_path = self.output_dir_eda / "height_by_class_boxplot.png"
        plt.savefig(output_path, dpi=150) #type: ignore
        plt.close()
        return output_path
    
    def save_pixel_intensity_histogram(self) -> Path:
        """Save a grayscale pixel intensity histogram from sampled images."""
        readable = self._require_readable_images()
        sample = readable.head(PIXEL_ANALYSIS_SAMPLE_SIZE)
        intensity_values = []
    
        for _, row in sample.iterrows(): #type: ignore
            grayscale = cv2.imread(str(row["file_path"]), cv2.IMREAD_GRAYSCALE) #type: ignore
            if grayscale is not None:
                intensity_values.extend(grayscale.flatten().tolist()) #type: ignore
    
        if not intensity_values:
            raise ValueError("No readable pixels were available for intensity analysis.")
    
        plt.figure(figsize=(9, 6)) #type: ignore
        sns.histplot(intensity_values, bins=50, color="#B279A2") #type: ignore
        plt.title("Sampled Grayscale Pixel Intensity Distribution") #type: ignore
        plt.xlabel("Pixel intensity, 0 dark to 255 bright") #type: ignore
        plt.ylabel("Frequency") #type: ignore
        plt.tight_layout()
    
        output_path = self.output_dir_eda / "pixel_intensity_histogram.png"
        plt.savefig(output_path, dpi=150) #type: ignore
        plt.close()
        return output_path
    
    def save_image_quality_issues(self) -> Path:
        """Save image quality flags to CSV."""
        records = []
        for _, row in self.filterd_dataframe.iterrows(): #type: ignore
            issues = []
            if not bool(row["readable"]): #type: ignore
                issues.append("unreadable_or_corrupted") #type: ignore
            if bool(row["readable"]) and ( #type: ignore
                row["width"] < VERY_SMALL_IMAGE_THRESHOLD[0]
                or row["height"] < VERY_SMALL_IMAGE_THRESHOLD[1]
            ):
                issues.append("very_small_image") #type: ignore
            if bool(row["readable"]) and ( #type: ignore
                row["aspect_ratio"] < UNUSUAL_ASPECT_RATIO_LOW
                or row["aspect_ratio"] > UNUSUAL_ASPECT_RATIO_HIGH
            ):
                issues.append("unusual_aspect_ratio") #type: ignore
    
            if issues:
                records.append( #type: ignore
                    {
                        "file_path": row["file_path"],
                        "label": row["label"],
                        "width": row["width"],
                        "height": row["height"],
                        "aspect_ratio": row["aspect_ratio"],
                        "issues": "; ".join(issues), #type: ignore
                    }
                )
    
        issues_dataframe = pd.DataFrame(
            records,
            columns=[
                "file_path",
                "label",
                "width",
                "height",
                "aspect_ratio",
                "issues",
            ],
        )
        issues_dataframe.to_csv(QUALITY_ISSUES_PATH, index=False)
        return QUALITY_ISSUES_PATH
    
    def save_class_imbalance_report(self) -> Path:
        """Save a written class imbalance report."""
        class_counts = self.filterd_dataframe["label"].value_counts().sort_values(  #type: ignore
            ascending=False
        )
        largest_class = class_counts.idxmax()
        smallest_class = class_counts.idxmin()
        largest_count = int(class_counts.max())
        smallest_count = int(class_counts.min())
        ratio = largest_count / smallest_count if smallest_count > 0 else float("inf")
    
        explanation = (
            "The class balance should be considered before any future Stage 2 "
            "classification work. A high imbalance ratio can bias a model towards "
            "the most common class and make minority macroinvertebrate classes "
            "harder to recognise."
        )
    
        report = [
            "# Class Imbalance Report",
            "",
            f"- Largest class: **{largest_class}** ({largest_count} images)",
            f"- Smallest class: **{smallest_class}** ({smallest_count} images)",
            f"- Imbalance ratio: **{ratio:.2f}:1**",
            "",
            "## Interpretation",
            "",
            explanation,
            "",
            "## Stage 2 Implication",
            "",
            (
                "For future modelling, consider stratified train/test splitting "
                "and class-aware evaluation metrics. If the imbalance is large, "
                "data collection, augmentation, or weighted evaluation may be "
                "needed."
            ),
        ]
    
        CLASS_IMBALANCE_REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
        return CLASS_IMBALANCE_REPORT_PATH
    
    def save_stage2_recommendations(self) -> Path:
        """Save EDA-based recommendations for future Stage 2 planning."""
        readable = self._require_readable_images()
        class_counts = self.filterd_dataframe["label"].value_counts()
        width_range = int(readable["width"].max() - readable["width"].min()) #type: ignore
        height_range = int(readable["height"].max() - readable["height"].min()) #type: ignore
        unreadable_count = int((~self.filterd_dataframe["readable"]).sum())
        quality_issues = self._build_quality_issues_dataframe()
    
        smallest_class_count = int(class_counts.min())
        largest_class_count = int(class_counts.max())
        imbalance_ratio = largest_class_count / smallest_class_count
        intensity_note = self._get_pixel_intensity_recommendation(readable)
    
        report = [
            "# Stage 2 Planning Recommendations",
            "",
            "This project does not implement Stage 2 classification or modelling. "
            "The recommendations below explain how the Stage 1 EDA would inform "
            "future preprocessing and model planning.",
            "",
            "## Resizing",
            "",
            (
                f"Readable images vary by {width_range} pixels in width and "
                f"{height_range} pixels in height. Future Stage 2 work should "
                "resize images to a consistent input size before modelling."
            ),
            "",
            "## Normalisation and Colour Processing",
            "",
            intensity_note,
            "",
            "## Class Imbalance",
            "",
            (
                f"The largest class has {largest_class_count} images and the "
                f"smallest class has {smallest_class_count} images, giving an "
                f"imbalance ratio of {imbalance_ratio:.2f}:1. A stratified "
                "train/test split is recommended so every class is represented "
                "fairly in evaluation."
            ),
            "",
            "## Data Cleaning",
            "",
            (
                f"The index found {unreadable_count} unreadable files and "
                f"{len(quality_issues)} total quality issue rows. Future Stage 2 "
                "work should review corrupted, very small, or unusual-aspect-ratio "
                "images before training."
            ),
            "",
            "## Recommended Future Stage 2 Workflow",
            "",
            "1. Clean or remove unreadable and severely inconsistent images.",
            "2. Resize images to a fixed shape suitable for the chosen method.",
            "3. Apply pixel normalisation after checking intensity distributions.",
            "4. Use a stratified train/test split.",
            "5. Track class-level results, not just overall accuracy.",
        ]
    
        STAGE2_RECOMMENDATIONS_PATH.write_text(
            "\n".join(report),
            encoding="utf-8",
        )
        return STAGE2_RECOMMENDATIONS_PATH
    
    def _require_readable_images(self) -> pd.DataFrame:
        """Return readable images or raise a useful error."""
        if self.readable_dataframe.empty:
            raise ValueError("No readable images were found for EDA charts.")
    
        return self.readable_dataframe
    
    def _select_representative_samples(self, readable: pd.DataFrame) -> pd.DataFrame:
        """Select up to one image per class, then fill remaining slots."""
        per_class = readable.groupby("label", group_keys=False).head(1) #type: ignore
        if len(per_class) >= SAMPLE_GRID_MAX_IMAGES:
            return per_class.head(SAMPLE_GRID_MAX_IMAGES)
    
        remaining_slots = SAMPLE_GRID_MAX_IMAGES - len(per_class)
        remaining = readable.drop(per_class.index).head(remaining_slots)
        return pd.concat([per_class, remaining])
    
    def _build_quality_issues_dataframe(self) -> pd.DataFrame:
        """Build quality issue rows without writing them."""
        records = []
        for _, row in self.filterd_dataframe.iterrows(): #type: ignore
            issue_count = 0
            if not bool(row["readable"]): #type: ignore
                issue_count += 1
            if bool(row["readable"]) and ( #type: ignore
                row["width"] < VERY_SMALL_IMAGE_THRESHOLD[0]
                or row["height"] < VERY_SMALL_IMAGE_THRESHOLD[1]
            ):
                issue_count += 1
            if bool(row["readable"]) and ( #type: ignore
                row["aspect_ratio"] < UNUSUAL_ASPECT_RATIO_LOW
                or row["aspect_ratio"] > UNUSUAL_ASPECT_RATIO_HIGH
            ):
                issue_count += 1
    
            if issue_count > 0:
                records.append(row.to_dict()) #type: ignore
    
        return pd.DataFrame(records)
    
    def _get_pixel_intensity_recommendation(self, readable: pd.DataFrame) -> str:
        """Create a short recommendation based on sampled grayscale intensity."""
        sample = readable.head(PIXEL_ANALYSIS_SAMPLE_SIZE)
        image_means = []
        image_standard_deviations = []
    
        for _, row in sample.iterrows(): #type: ignore
            grayscale = cv2.imread(str(row["file_path"]), cv2.IMREAD_GRAYSCALE) #type: ignore
            if grayscale is None:
                continue

            grayscale = np.asarray(grayscale)

            image_means.append(float(grayscale.mean())) #type: ignore
            image_standard_deviations.append(grayscale.mean()) #type: ignore
    
        if not image_means:
            return (
                "Pixel intensity analysis could not be completed because no "
                "readable sample images were available."
            )
    
        mean_intensity = float(np.mean(image_means)) #type: ignore
        mean_contrast = float(np.mean(image_standard_deviations)) #type: ignore
        return (
            f"The sampled grayscale images have an average intensity of "
            f"{mean_intensity:.1f} and average contrast of {mean_contrast:.1f}. "
            "Future Stage 2 preprocessing should consider normalising pixel "
            "values. Grayscale conversion may be useful if colour is not a "
            "reliable feature for the macroinvertebrate classes, but this should "
            "be compared against colour-based inputs."
        )
    
    def _format_class_counts(self, class_counts: pd.Series[Any]) -> str:
        """Format class counts into a readable summary value."""
        return "; ".join(
            f"{label}: {count}" for label, count in class_counts.items()
        )
    
    def _safe_round(self, value: float) -> float:
        """Round a numeric value while handling missing data."""
        if pd.isna(value): #type: ignore
            return 0.0
    
        return round(float(value), 2)
    
    def _safe_int(self, value: float) -> int:
        """Convert a numeric value to int while handling missing data."""
        if pd.isna(value): #type: ignore
            return 0
    
        return int(value)