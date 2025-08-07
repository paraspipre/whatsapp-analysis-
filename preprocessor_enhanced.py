import re
import pandas as pd
import streamlit as st
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

def preprocess_enhanced(data: str) -> Tuple[Optional[pd.DataFrame], str]:
    """
    Enhanced preprocessing function with better error handling and debugging
    
    Args:
        data: Raw WhatsApp chat export text
        
    Returns:
        Tuple of (dataframe, error_message)
    """
    try:
        # First, let's check if the data is not empty
        if not data or len(data.strip()) == 0:
            return None, "Uploaded file is empty"
        
        # Try different date patterns for WhatsApp exports
        patterns = [
            # Standard WhatsApp format: 12/25/23, 2:30 PM - 
            r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s',
            # Alternative format: 25/12/2023, 14:30 - 
            r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s-\s',
            # Another format: 2023-12-25, 14:30 - 
            r'\d{4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\s-\s',
            # 24-hour format: 12/25/23, 14:30 - 
            r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
            # DD/MM/YY format: 13/06/25, 10:04 - 
            r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        ]
        
        pattern_found = False
        selected_pattern = None
        date_format = None
        
        for i, pattern in enumerate(patterns):
            if re.search(pattern, data):
                selected_pattern = pattern
                pattern_found = True
                
                # Set appropriate date format based on pattern
                if i == 0:  # Standard format
                    date_format = '%m/%d/%y, %I:%M %p - '
                elif i == 1:  # Alternative format
                    date_format = '%d/%m/%Y, %H:%M - '
                elif i == 2:  # ISO format
                    date_format = '%Y-%m-%d, %H:%M - '
                elif i == 3:  # 24-hour format
                    date_format = '%m/%d/%y, %H:%M - '
                elif i == 4:  # DD/MM/YY format (day first)
                    date_format = '%d/%m/%y, %H:%M - '
                break
        
        if not pattern_found:
            # If no pattern found, let's show some debug info
            first_lines = data[:500]  # First 500 characters
            return None, f"No valid date pattern found. First 500 characters: {first_lines}"
        
        # Split messages and extract dates
        messages = re.split(selected_pattern, data)[1:]
        dates = re.findall(selected_pattern, data)
        
        # Debug info
        st.info(f"Found {len(messages)} messages and {len(dates)} dates")
        
        if len(messages) == 0:
            return None, "No messages found after splitting"
        
        if len(dates) == 0:
            return None, "No dates found in the file"
        
        # Create dataframe
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        
        # Convert dates with error handling
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format=date_format)
        except Exception as e:
            # If the specific format fails, try different approaches
            clean_dates = [date.rstrip(' -') for date in df['message_date']]
            
            # Try MM/DD/YY format first
            try:
                df['message_date'] = pd.to_datetime(clean_dates, format='%m/%d/%y, %H:%M')
            except Exception as e2:
                # Try DD/MM/YY format (day first)
                try:
                    df['message_date'] = pd.to_datetime(clean_dates, format='%d/%m/%y, %H:%M', dayfirst=True)
                except Exception as e3:
                    # Last resort: try with dayfirst=True
                    df['message_date'] = pd.to_datetime(clean_dates, dayfirst=True)
        
        df.rename(columns={'message_date': 'date'}, inplace=True)
        
        # Extract users and messages
        users = []
        clean_messages = []
        
        for message in df['user_message']:
            if not message or message.strip() == '':
                continue
                
            # Try different patterns for user extraction
            user_patterns = [
                r'^([^:]+):\s*(.*)',  # Standard: User: Message
                r'^([^:]+):(.*)',     # No space after colon
                r'^([^-]+)-\s*(.*)'   # Alternative: User - Message
            ]
            
            user_found = False
            for user_pattern in user_patterns:
                match = re.match(user_pattern, message.strip())
                if match:
                    users.append(match.group(1).strip())
                    clean_messages.append(match.group(2).strip())
                    user_found = True
                    break
            
            if not user_found:
                # If no user pattern matches, treat as group notification
                users.append('group_notification')
                clean_messages.append(message.strip())
        
        df['user'] = users
        df['message'] = clean_messages
        
        # Remove media messages after creating the message column
        df = df[df['message'] != '<Media omitted>']
        df.drop(columns=['user_message'], inplace=True)
        
        # Remove rows with empty messages
        df = df[df['message'].str.len() > 0]
        
        if df.empty:
            return None, "No valid messages found after processing"
        
        # Add time-based columns
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        
        # Create period column
        period = []
        for hour in df['hour']:
            if hour == 23:
                period.append(f"{hour}-00")
            elif hour == 0:
                period.append(f"00-{hour + 1}")
            else:
                period.append(f"{hour}-{hour + 1}")
        
        df['period'] = period
        
        # Final validation
        if df.empty:
            return None, "DataFrame is empty after processing"
        
        if df['user'].nunique() == 0:
            return None, "No users found in the processed data"
        
        st.success(f"Successfully processed {len(df)} messages from {df['user'].nunique()} users")
        
        return df, ""
        
    except Exception as e:
        logger.error(f"Error in preprocessing: {str(e)}")
        return None, f"Error during preprocessing: {str(e)}"

def debug_file_content(data: str) -> None:
    """
    Debug function to show file content structure
    
    Args:
        data: Raw file content
    """
    st.markdown("### 🔍 File Content Debug")
    
    # Show first few lines
    lines = data.split('\n')[:10]
    st.text("First 10 lines:")
    for i, line in enumerate(lines):
        st.text(f"{i+1}: {line}")
    
    # Show file statistics
    st.markdown(f"**File Statistics:**")
    st.markdown(f"- Total characters: {len(data)}")
    st.markdown(f"- Total lines: {len(data.split('\n'))}")
    st.markdown(f"- Non-empty lines: {len([line for line in data.split('\n') if line.strip()])}")
    
    # Check for common patterns
    patterns_to_check = [
        (r'\d{1,2}/\d{1,2}/\d{2,4}', "Date pattern (MM/DD/YY)"),
        (r'\d{1,2}/\d{1,2}/\d{4}', "Date pattern (MM/DD/YYYY)"),
        (r'\d{1,2}:\d{2}\s[AP]M', "Time pattern (12-hour)"),
        (r'\d{1,2}:\d{2}', "Time pattern (24-hour)"),
        (r'[^:]+:\s', "User pattern"),
    ]
    
    st.markdown("**Pattern Analysis:**")
    for pattern, description in patterns_to_check:
        matches = re.findall(pattern, data)
        st.markdown(f"- {description}: {len(matches)} matches")
        if matches:
            st.markdown(f"  - Examples: {matches[:3]}")

# Keep the original function for backward compatibility
def preprocess(data):
    """
    Original preprocessing function - now calls the enhanced version
    """
    df, error = preprocess_enhanced(data)
    if error:
        raise ValueError(error)
    return df 