import re
import pandas as pd

def preprocess(data):
    # Try different date patterns for WhatsApp exports
    patterns = [
        # Standard WhatsApp format: 12/25/23, 2:30 PM - 
        r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s',
        # 24-hour format: 06/06/25, 19:29 - 
        r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        # Alternative format: 25/12/2023, 14:30 - 
        r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s-\s',
        # Another format: 2023-12-25, 14:30 - 
        r'\d{4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\s-\s'
    ]
    
    pattern_found = False
    selected_pattern = None
    date_format = None
    
    for i, pattern in enumerate(patterns):
        if re.search(pattern, data):
            selected_pattern = pattern
            pattern_found = True
            
            # Set appropriate date format based on pattern
            if i == 0:  # Standard format with AM/PM
                date_format = '%m/%d/%y, %I:%M %p - '
            elif i == 1:  # 24-hour format
                date_format = '%m/%d/%y, %H:%M - '
            elif i == 2:  # Alternative format
                date_format = '%d/%m/%Y, %H:%M - '
            elif i == 3:  # ISO format
                date_format = '%Y-%m-%d, %H:%M - '
            break
    
    if not pattern_found:
        raise ValueError("No valid date pattern found in the file")
    
    messages = re.split(selected_pattern, data)[1:]
    dates = re.findall(selected_pattern, data)

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

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df