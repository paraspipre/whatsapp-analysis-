import streamlit as st
import pandas as pd
from typing import Optional, Tuple
import logging
from config import UPLOAD_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppAnalysisError(Exception):
    """Custom exception for WhatsApp analysis errors"""
    pass

def validate_uploaded_file(uploaded_file) -> Tuple[bool, str]:
    """
    Validate the uploaded WhatsApp chat file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file size
    if uploaded_file.size > UPLOAD_CONFIG["max_file_size"]:
        return False, f"File too large. Maximum size is {UPLOAD_CONFIG['max_file_size'] // (1024*1024)}MB"
    
    # Check file type
    if not uploaded_file.name.lower().endswith('.txt'):
        return False, "Please upload a .txt file"
    
    return True, ""

def safe_file_read(uploaded_file) -> Optional[str]:
    """
    Safely read uploaded file with error handling
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        File content as string or None if error
    """
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode(UPLOAD_CONFIG["encoding"])
        return data
    except UnicodeDecodeError:
        st.error("Error reading file. Please ensure the file is UTF-8 encoded.")
        return None
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        st.error(f"Error reading file: {str(e)}")
        return None

def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate the processed dataframe
    
    Args:
        df: Processed WhatsApp chat dataframe
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if df is None or df.empty:
        return False, "No data found in the uploaded file"
    
    required_columns = ['user', 'message', 'date']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {missing_columns}"
    
    if df['user'].nunique() == 0:
        return False, "No users found in the chat data"
    
    return True, ""

def handle_analysis_error(func):
    """
    Decorator to handle analysis function errors gracefully
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            st.error(f"An error occurred during analysis: {str(e)}")
            return None
    return wrapper

def show_loading_spinner(message: str = "Processing..."):
    """
    Show a loading spinner with custom message
    """
    return st.spinner(message)

def display_error_message(error: str):
    """
    Display error message with consistent styling
    """
    st.error(f"❌ {error}")

def display_success_message(message: str):
    """
    Display success message with consistent styling
    """
    st.success(f"✅ {message}")

def format_number(num: int) -> str:
    """
    Format large numbers with K, M suffixes
    """
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num) 