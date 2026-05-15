from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
OUTPUTS_DIR = BASE_DIR / "outputs"
EDA_OUTPUT_DIR = OUTPUTS_DIR / "eda"
MODEL_OUTPUT_DIR = OUTPUTS_DIR / "models"
IMAGE_SIZE = (128, 128)
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

#this are constants that apeared in Pranavs example code for the EDA functions
#i will try my best to give them realistic values, but i dont know what alot of them are for
REPORT_OUTPUT_DIR = BASE_DIR / "reports"
CLASS_IMBALANCE_REPORT_PATH = REPORT_OUTPUT_DIR/"class_imbalance_report.csv"
PIXEL_ANALYSIS_SAMPLE_SIZE = 500
QUALITY_ISSUES_PATH = REPORT_OUTPUT_DIR/"quality_issues.csv"

SAMPLE_GRID_MAX_IMAGES = 64
STAGE2_RECOMMENDATIONS_PATH = REPORT_OUTPUT_DIR/"stage2_recommendations.json"
UNUSUAL_ASPECT_RATIO_HIGH = 3.0
UNUSUAL_ASPECT_RATIO_LOW = 0.33
VERY_SMALL_IMAGE_THRESHOLD = (64, 64)