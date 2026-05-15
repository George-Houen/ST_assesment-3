from pathlib import Path
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns
import numpy as np

class EDAService:
    """Generate and save EDA outputs for the indexed image dataset."""
    def __init__(self, dataframe: pd.DataFrame, output_dir: Path) -> None:
        self.base_dataframe : pd.DataFrame = dataframe         
        self.output_dir = output_dir
        print(output_dir)
        self.filterd_dataframe: pd.DataFrame = dataframe
    
    def filter_data_frame(self, labels:list[str]):
        print(labels)
        self.filterd_dataframe = self.base_dataframe[self.base_dataframe["label"].isin(labels)]

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
    

    #following functions provided from Pranav by email with permision:

    def generate_width_height_scatter_plot(self) -> Path:
        """Save a scatter plot of image width versus height."""
        readable = self._require_readable_images()
    
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=readable, x="width", y="height", hue="label", alpha=0.75)
        plt.title("Image Width Versus Height")
        plt.xlabel("Width in pixels")
        plt.ylabel("Height in pixels")
        plt.legend(title="Class", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
    
        output_path = self.output_dir / "width_height_scatter.png"
        plt.savefig(output_path, dpi=150)
        plt.close()
        return output_path
    
    def generate_sample_image_grid(self) -> Path:
        """Save a grid of representative readable sample images."""
        readable = self._require_readable_images()
        samples = self._select_representative_samples(readable)
    
        columns = min(4, len(samples))
        rows = int(np.ceil(len(samples) / columns))
        fig, axes = plt.subplots(rows, columns, figsize=(4 * columns, 3.4 * rows))
        axes_array = np.array(axes).reshape(-1)
    
        for axis in axes_array:
            axis.axis("off")
    
        for axis, (_, row) in zip(axes_array, samples.iterrows()):
            image = cv2.imread(str(row["file_path"]), cv2.IMREAD_COLOR)
            if image is None:
                continue
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            axis.imshow(rgb_image)
            axis.set_title(str(row["label"]), fontsize=10)
            axis.axis("off")
    
        fig.suptitle("Representative Sample Images by Class")
        fig.tight_layout()
        output_path = self.output_dir / "sample_image_grid.png"
        fig.savefig(output_path, dpi=150)
        plt.close(fig)
        return output_path
    
    def generate_width_by_class_boxplot(self) -> Path:
        """Save a boxplot comparing image widths by class."""
        readable = self._require_readable_images()
    
        plt.figure(figsize=(11, 6))
        sns.boxplot(data=readable, x="label", y="width", color="#72B7B2")
        plt.title("Image Width by Class")
        plt.xlabel("Class label")
        plt.ylabel("Width in pixels")
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()
    
        output_path = self.output_dir / "width_by_class_boxplot.png"
        plt.savefig(output_path, dpi=150)
        plt.close()
        return output_path
    
    def generate_height_by_class_boxplot(self) -> Path:
        """Save a boxplot comparing image heights by class."""
        readable = self._require_readable_images()
    
        plt.figure(figsize=(11, 6))
        sns.boxplot(data=readable, x="label", y="height", color="#54A24B")
        plt.title("Image Height by Class")
        plt.xlabel("Class label")
        plt.ylabel("Height in pixels")
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()
    
        output_path = self.output_dir / "height_by_class_boxplot.png"
        plt.savefig(output_path, dpi=150)
        plt.close()
        return output_path
    
    def generate_pixel_intensity_histogram(self) -> Path:
        """Save a grayscale pixel intensity histogram from sampled images."""
        readable = self._require_readable_images()
        sample = readable.head(PIXEL_ANALYSIS_SAMPLE_SIZE)
        intensity_values = []
    
        for _, row in sample.iterrows():
            grayscale = cv2.imread(str(row["file_path"]), cv2.IMREAD_GRAYSCALE)
            if grayscale is not None:
                intensity_values.extend(grayscale.flatten().tolist())
    
        if not intensity_values:
            raise ValueError("No readable pixels were available for intensity analysis.")
    
        plt.figure(figsize=(9, 6))
        sns.histplot(intensity_values, bins=50, color="#B279A2")
        plt.title("Sampled Grayscale Pixel Intensity Distribution")
        plt.xlabel("Pixel intensity, 0 dark to 255 bright")
        plt.ylabel("Frequency")
        plt.tight_layout()
    
        output_path = self.output_dir / "pixel_intensity_histogram.png"
        plt.savefig(output_path, dpi=150)
        plt.close()
        return output_path
    
    def generate_image_quality_issues(self) -> Path:
        """Save image quality flags to CSV."""
        records = []
        for _, row in self.dataframe.iterrows():
            issues = []
            if not bool(row["readable"]):
                issues.append("unreadable_or_corrupted")
            if bool(row["readable"]) and (
                row["width"] < VERY_SMALL_IMAGE_THRESHOLD
                or row["height"] < VERY_SMALL_IMAGE_THRESHOLD
            ):
                issues.append("very_small_image")
            if bool(row["readable"]) and (
                row["aspect_ratio"] < UNUSUAL_ASPECT_RATIO_LOW
                or row["aspect_ratio"] > UNUSUAL_ASPECT_RATIO_HIGH
            ):
                issues.append("unusual_aspect_ratio")
    
            if issues:
                records.append(
                    {
                        "file_path": row["file_path"],
                        "label": row["label"],
                        "width": row["width"],
                        "height": row["height"],
                        "aspect_ratio": row["aspect_ratio"],
                        "issues": "; ".join(issues),
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
    
    def generate_class_imbalance_report(self) -> Path:
        """Save a written class imbalance report."""
        class_counts = self.dataframe["label"].value_counts().sort_values(
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
    
    def generate_stage2_recommendations(self) -> Path:
        """Save EDA-based recommendations for future Stage 2 planning."""
        readable = self._require_readable_images()
        class_counts = self.dataframe["label"].value_counts()
        width_range = int(readable["width"].max() - readable["width"].min())
        height_range = int(readable["height"].max() - readable["height"].min())
        unreadable_count = int((~self.dataframe["readable"]).sum())
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
        per_class = readable.groupby("label", group_keys=False).head(1)
        if len(per_class) >= SAMPLE_GRID_MAX_IMAGES:
            return per_class.head(SAMPLE_GRID_MAX_IMAGES)
    
        remaining_slots = SAMPLE_GRID_MAX_IMAGES - len(per_class)
        remaining = readable.drop(per_class.index).head(remaining_slots)
        return pd.concat([per_class, remaining])
    
    def _build_quality_issues_dataframe(self) -> pd.DataFrame:
        """Build quality issue rows without writing them."""
        records = []
        for _, row in self.dataframe.iterrows():
            issue_count = 0
            if not bool(row["readable"]):
                issue_count += 1
            if bool(row["readable"]) and (
                row["width"] < VERY_SMALL_IMAGE_THRESHOLD
                or row["height"] < VERY_SMALL_IMAGE_THRESHOLD
            ):
                issue_count += 1
            if bool(row["readable"]) and (
                row["aspect_ratio"] < UNUSUAL_ASPECT_RATIO_LOW
                or row["aspect_ratio"] > UNUSUAL_ASPECT_RATIO_HIGH
            ):
                issue_count += 1
    
            if issue_count > 0:
                records.append(row.to_dict())
    
        return pd.DataFrame(records)
    
    def _get_pixel_intensity_recommendation(self, readable: pd.DataFrame) -> str:
        """Create a short recommendation based on sampled grayscale intensity."""
        sample = readable.head(PIXEL_ANALYSIS_SAMPLE_SIZE)
        image_means = []
        image_standard_deviations = []
    
        for _, row in sample.iterrows():
            grayscale = cv2.imread(str(row["file_path"]), cv2.IMREAD_GRAYSCALE)
            if grayscale is not None:
                image_means.append(float(np.mean(grayscale)))
                image_standard_deviations.append(float(np.std(grayscale)))
    
        if not image_means:
            return (
                "Pixel intensity analysis could not be completed because no "
                "readable sample images were available."
            )
    
        mean_intensity = float(np.mean(image_means))
        mean_contrast = float(np.mean(image_standard_deviations))
        return (
            f"The sampled grayscale images have an average intensity of "
            f"{mean_intensity:.1f} and average contrast of {mean_contrast:.1f}. "
            "Future Stage 2 preprocessing should consider normalising pixel "
            "values. Grayscale conversion may be useful if colour is not a "
            "reliable feature for the macroinvertebrate classes, but this should "
            "be compared against colour-based inputs."
        )
    
    def _format_class_counts(self, class_counts: pd.Series) -> str:
        """Format class counts into a readable summary value."""
        return "; ".join(
            f"{label}: {count}" for label, count in class_counts.items()
        )
    
    def _safe_round(self, value: float) -> float:
        """Round a numeric value while handling missing data."""
        if pd.isna(value):
            return 0.0
    
        return round(float(value), 2)
    
    def _safe_int(self, value: float) -> int:
        """Convert a numeric value to int while handling missing data."""
        if pd.isna(value):
            return 0
    
        return int(value)