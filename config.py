import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
STOP_WORDS_FILE = PROJECT_ROOT / "stop_hinglish.txt"

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": "WhatsApp Chat Analyzer",
    "page_icon": "📱",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Analysis settings
ANALYSIS_CONFIG = {
    "max_common_words": 20,
    "wordcloud_width": 500,
    "wordcloud_height": 500,
    "wordcloud_min_font_size": 10,
    "wordcloud_background_color": "white",
    "heatmap_figsize": (10, 6),
    "timeline_figsize": (12, 6)
}

# Chart colors
CHART_COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e", 
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff7f0e",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# File upload settings
UPLOAD_CONFIG = {
    "max_file_size": 200 * 1024 * 1024,  # 200MB
    "allowed_types": ["txt"],
    "encoding": "utf-8"
} 