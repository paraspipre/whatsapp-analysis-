import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from collections import Counter
from typing import Dict, List, Tuple
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import handle_analysis_error

class AdvancedAnalyzer:
    """Advanced analysis features for WhatsApp chat data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.stop_words = self._load_stop_words()
    
    def _load_stop_words(self) -> set:
        """Load stop words from file"""
        try:
            with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
                return set(f.read().split('\n'))
        except FileNotFoundError:
            return set()
    
    @handle_analysis_error
    def sentiment_analysis(self, selected_user: str = 'Overall') -> pd.DataFrame:
        """
        Perform sentiment analysis on messages
        
        Args:
            selected_user: User to analyze or 'Overall' for all users
            
        Returns:
            DataFrame with sentiment scores
        """
        if selected_user != 'Overall':
            df = self.df[self.df['user'] == selected_user]
        else:
            df = self.df.copy()
        
        # Filter out media messages and notifications
        df = df[df['message'] != '<Media omitted>\n']
        df = df[df['user'] != 'group_notification']
        
        # Calculate sentiment scores
        sentiments = []
        for message in df['message']:
            blob = TextBlob(message)
            sentiments.append(blob.sentiment.polarity)
        
        df['sentiment'] = sentiments
        
        # Aggregate by date
        daily_sentiment = df.groupby('only_date')['sentiment'].agg(['mean', 'count']).reset_index()
        daily_sentiment.columns = ['date', 'avg_sentiment', 'message_count']
        
        return daily_sentiment
    
    @handle_analysis_error
    def message_patterns(self, selected_user: str = 'Overall') -> Dict:
        """
        Analyze message patterns and timing
        
        Args:
            selected_user: User to analyze or 'Overall' for all users
            
        Returns:
            Dictionary with pattern analysis results
        """
        if selected_user != 'Overall':
            df = self.df[self.df['user'] == selected_user]
        else:
            df = self.df.copy()
        
        patterns = {}
        
        # Most active hours
        patterns['hourly_activity'] = df['hour'].value_counts().sort_index()
        
        # Response time analysis (if multiple users)
        if selected_user == 'Overall' and df['user'].nunique() > 1:
            patterns['response_times'] = self._analyze_response_times(df)
        
        # Message length patterns
        df['message_length'] = df['message'].str.len()
        patterns['avg_message_length'] = df['message_length'].mean()
        patterns['message_length_distribution'] = df['message_length'].describe()
        
        # Typing patterns (messages sent in quick succession)
        patterns['typing_patterns'] = self._analyze_typing_patterns(df)
        
        return patterns
    
    def _analyze_response_times(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze response times between users"""
        # Sort by timestamp
        df_sorted = df.sort_values('date')
        
        response_times = []
        for i in range(1, len(df_sorted)):
            current_msg = df_sorted.iloc[i]
            prev_msg = df_sorted.iloc[i-1]
            
            if current_msg['user'] != prev_msg['user']:
                time_diff = (current_msg['date'] - prev_msg['date']).total_seconds() / 60  # minutes
                if time_diff < 60:  # Only consider responses within 1 hour
                    response_times.append({
                        'responder': current_msg['user'],
                        'responded_to': prev_msg['user'],
                        'response_time_minutes': time_diff
                    })
        
        return pd.DataFrame(response_times)
    
    def _analyze_typing_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze typing patterns and message bursts"""
        df_sorted = df.sort_values('date')
        
        # Find message bursts (messages sent within 30 seconds)
        bursts = []
        current_burst = [df_sorted.iloc[0]]
        
        for i in range(1, len(df_sorted)):
            current_msg = df_sorted.iloc[i]
            last_msg = current_burst[-1]
            
            time_diff = (current_msg['date'] - last_msg['date']).total_seconds()
            
            if time_diff <= 30 and current_msg['user'] == last_msg['user']:
                current_burst.append(current_msg)
            else:
                if len(current_burst) > 1:
                    bursts.append(current_burst)
                current_burst = [current_msg]
        
        if len(current_burst) > 1:
            bursts.append(current_burst)
        
        return {
            'total_bursts': len(bursts),
            'avg_burst_size': np.mean([len(burst) for burst in bursts]) if bursts else 0,
            'max_burst_size': max([len(burst) for burst in bursts]) if bursts else 0
        }
    
    @handle_analysis_error
    def topic_modeling(self, selected_user: str = 'Overall', num_topics: int = 5) -> Dict:
        """
        Basic topic modeling using word frequency analysis
        
        Args:
            selected_user: User to analyze or 'Overall' for all users
            num_topics: Number of topics to identify
            
        Returns:
            Dictionary with topic analysis results
        """
        if selected_user != 'Overall':
            df = self.df[self.df['user'] == selected_user]
        else:
            df = self.df.copy()
        
        # Filter messages
        df = df[df['message'] != '<Media omitted>\n']
        df = df[df['user'] != 'group_notification']
        
        # Extract words
        all_words = []
        for message in df['message']:
            words = re.findall(r'\b\w+\b', message.lower())
            words = [word for word in words if word not in self.stop_words and len(word) > 2]
            all_words.extend(words)
        
        # Find most common word combinations (bigrams)
        bigrams = []
        for message in df['message']:
            words = re.findall(r'\b\w+\b', message.lower())
            words = [word for word in words if word not in self.stop_words and len(word) > 2]
            for i in range(len(words) - 1):
                bigrams.append(f"{words[i]} {words[i+1]}")
        
        # Get top topics
        word_freq = Counter(all_words)
        bigram_freq = Counter(bigrams)
        
        return {
            'top_words': dict(word_freq.most_common(20)),
            'top_bigrams': dict(bigram_freq.most_common(10)),
            'total_unique_words': len(word_freq),
            'total_words': len(all_words)
        }
    
    @handle_analysis_error
    def user_interaction_network(self) -> Dict:
        """
        Analyze user interaction patterns
        
        Returns:
            Dictionary with interaction analysis
        """
        df_sorted = self.df.sort_values('date')
        
        interactions = []
        for i in range(1, len(df_sorted)):
            current_msg = df_sorted.iloc[i]
            prev_msg = df_sorted.iloc[i-1]
            
            if current_msg['user'] != prev_msg['user']:
                interactions.append({
                    'from_user': prev_msg['user'],
                    'to_user': current_msg['user'],
                    'timestamp': current_msg['date']
                })
        
        interaction_df = pd.DataFrame(interactions)
        
        if interaction_df.empty:
            return {'error': 'No interactions found'}
        
        # Count interactions
        interaction_counts = interaction_df.groupby(['from_user', 'to_user']).size().reset_index(name='count')
        
        # Find most interactive users
        user_interaction_counts = interaction_df.groupby('to_user').size().sort_values(ascending=False)
        
        return {
            'interaction_matrix': interaction_counts,
            'most_interactive_users': user_interaction_counts.to_dict(),
            'total_interactions': len(interactions)
        }
    
    @handle_analysis_error
    def media_analysis(self, selected_user: str = 'Overall') -> Dict:
        """
        Analyze media sharing patterns
        
        Args:
            selected_user: User to analyze or 'Overall' for all users
            
        Returns:
            Dictionary with media analysis results
        """
        if selected_user != 'Overall':
            df = self.df[self.df['user'] == selected_user]
        else:
            df = self.df.copy()
        
        # Count media messages
        media_messages = df[df['message'] == '<Media omitted>\n']
        
        # Analyze media patterns by time
        media_by_hour = media_messages['hour'].value_counts().sort_index()
        media_by_day = media_messages['day_name'].value_counts()
        media_by_month = media_messages['month'].value_counts()
        
        return {
            'total_media': len(media_messages),
            'media_percentage': (len(media_messages) / len(df)) * 100,
            'media_by_hour': media_by_hour.to_dict(),
            'media_by_day': media_by_day.to_dict(),
            'media_by_month': media_by_month.to_dict(),
            'media_timeline': media_messages.groupby('only_date').size().reset_index(name='count')
        } 