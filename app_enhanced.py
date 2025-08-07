import streamlit as st
import pandas as pd
from typing import Optional

# Import custom modules
import preprocessor
import preprocessor_enhanced
import helper
from utils import (
    validate_uploaded_file, 
    safe_file_read, 
    validate_dataframe, 
    display_error_message,
    display_success_message,
    show_loading_spinner
)
from ui_components import UIComponents
from advanced_analysis import AdvancedAnalyzer
from config import STREAMLIT_CONFIG

# Configure Streamlit page
st.set_page_config(
    page_title=STREAMLIT_CONFIG["page_title"],
    page_icon=STREAMLIT_CONFIG["page_icon"],
    layout=STREAMLIT_CONFIG["layout"],
    initial_sidebar_state=STREAMLIT_CONFIG["initial_sidebar_state"]
)

def main():
    """Main application function"""
    
    # Create header
    UIComponents.create_header()
    
    # Create sidebar and get uploaded file
    uploaded_file = UIComponents.create_sidebar()
    
    if uploaded_file is not None:
        # Validate uploaded file
        is_valid, error_message = validate_uploaded_file(uploaded_file)
        
        if not is_valid:
            display_error_message(error_message)
            return
        
        # Read file safely
        data = safe_file_read(uploaded_file)
        if data is None:
            return
        
        # Add debug option in sidebar
        debug_mode = st.sidebar.checkbox("🔧 Debug Mode", help="Enable to see detailed processing information")
        
        if debug_mode:
            preprocessor_enhanced.debug_file_content(data)
        
        # Process data with loading spinner
        with show_loading_spinner("Processing chat data..."):
            try:
                # Use enhanced preprocessor
                df, error = preprocessor_enhanced.preprocess_enhanced(data)
                if error:
                    display_error_message(f"Error processing file: {error}")
                    return
            except Exception as e:
                display_error_message(f"Error processing file: {str(e)}")
                return
        
        # Validate processed dataframe
        is_valid, error_message = validate_dataframe(df)
        if not is_valid:
            display_error_message(error_message)
            return
        
        display_success_message("Chat data processed successfully!")
        
        # Get unique users
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")
        
        # Create user selector
        selected_user = UIComponents.create_user_selector(user_list)
        
        # Analysis button
        if st.sidebar.button("🚀 Start Analysis", type="primary"):
            run_analysis(df, selected_user, uploaded_file.name)
    
    else:
        # Show welcome message and instructions
        show_welcome_screen()

def show_welcome_screen():
    """Display welcome screen with instructions"""
    st.markdown("""
    ## 🎯 Welcome to WhatsApp Chat Analyzer!
    
    This tool helps you analyze your WhatsApp chat exports and discover interesting insights about your conversations.
    
    ### 📋 How to use:
    1. **Export your WhatsApp chat:**
       - Open WhatsApp Web or mobile app
       - Go to the chat you want to analyze
       - Export chat (without media) as a .txt file
       
    2. **Upload the file:**
       - Use the file uploader in the sidebar
       - Select the exported .txt file
       
    3. **Choose analysis options:**
       - Select a specific user or analyze the entire chat
       - Click "Start Analysis" to begin
       
    ### 🔍 What you'll discover:
    - **Message statistics** (total messages, words, media, links)
    - **Timeline analysis** (monthly and daily patterns)
    - **Activity patterns** (busy days, hours, heatmaps)
    - **User analysis** (most active users, interaction patterns)
    - **Text analysis** (word clouds, common words, emoji usage)
    - **Advanced features** (sentiment analysis, response times)
    
    ### 💡 Tips:
    - Larger chat files may take longer to process
    - For best results, export chats without media files
    - The analysis works with both individual and group chats
    """)
    
    # Add some example visualizations or screenshots here
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📊 **Message Statistics**\n\nView total messages, words, media shared, and links")
    
    with col2:
        st.info("📈 **Timeline Analysis**\n\nSee how conversation activity changes over time")
    
    with col3:
        st.info("👥 **User Insights**\n\nDiscover who's most active and interaction patterns")

def run_analysis(df: pd.DataFrame, selected_user: str, filename: str):
    """Run the complete analysis"""
    
    # Initialize advanced analyzer
    advanced_analyzer = AdvancedAnalyzer(df)
    
    # Create tabs for different analysis sections
    overview_tab, timeline_tab, user_tab, text_tab, advanced_tab = UIComponents.create_tabs()
    
    with overview_tab:
        show_overview_analysis(df, selected_user)
    
    with timeline_tab:
        show_timeline_analysis(df, selected_user)
    
    with user_tab:
        show_user_analysis(df, selected_user)
    
    with text_tab:
        show_text_analysis(df, selected_user)
    
    with advanced_tab:
        show_advanced_analysis(advanced_analyzer, selected_user)

def show_overview_analysis(df: pd.DataFrame, selected_user: str):
    """Display overview analysis"""
    st.markdown("## Overview Analysis")
    
    # Fetch basic statistics
    num_messages, words, num_links = helper.fetch_stats(selected_user, df)
    
    # Create stats cards
    stats = {
        'messages': num_messages,
        'words': words,
        'links': num_links
    }
    
    UIComponents.create_stats_cards(stats)
    
    # Additional metrics
    col1, col2 = st.columns(2)
    
    with col1:
        if selected_user == 'Overall':
            avg_messages_per_user = num_messages / df['user'].nunique()
            UIComponents.create_metric_card(
                "Avg Messages per User", 
                f"{avg_messages_per_user:.1f}"
            )
    
    with col2:
        avg_words_per_message = words / num_messages if num_messages > 0 else 0
        UIComponents.create_metric_card(
            "Avg Words per Message", 
            f"{avg_words_per_message:.1f}"
        )

def show_timeline_analysis(df: pd.DataFrame, selected_user: str):
    """Display timeline analysis"""
    st.markdown("## Timeline Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        UIComponents.create_timeline_chart(timeline, "Monthly Message Activity")
    
    with col2:
        st.markdown("### Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        UIComponents.create_timeline_chart(daily_timeline, "Daily Message Activity")
    
    # Activity maps
    st.markdown("### Activity Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Most Active Days")
        busy_day = helper.week_activity_map(selected_user, df)
        UIComponents.create_bar_chart(busy_day, "Messages by Day of Week", "#8B5CF6")
    
    with col2:
        st.markdown("#### Most Active Months")
        busy_month = helper.month_activity_map(selected_user, df)
        UIComponents.create_bar_chart(busy_month, "Messages by Month", "#F59E0B")
    
    # Weekly activity heatmap
    st.markdown("### Weekly Activity Heatmap")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    UIComponents.create_activity_heatmap(user_heatmap, "Activity by Day and Hour")

def show_user_analysis(df: pd.DataFrame, selected_user: str):
    """Display user analysis"""
    st.markdown("## User Analysis")
    
    if selected_user == 'Overall':
        # Most busy users
        st.markdown("### Most Active Users")
        x, new_df = helper.most_busy_users(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            UIComponents.create_bar_chart(x, "Messages by User", "#EF4444")
        
        with col2:
            st.markdown("#### User Statistics")
            st.dataframe(new_df, use_container_width=True)
            
            # Download button
            UIComponents.create_download_button(
                new_df, 
                "user_statistics.csv", 
                "Download User Statistics"
            )
    else:
        # Individual user analysis
        st.markdown(f"### Analysis for {selected_user}")
        
        # Get user-specific stats
        user_stats = df[df['user'] == selected_user]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            UIComponents.create_metric_card(
                "Total Messages", 
                str(len(user_stats))
            )
        
        with col2:
            avg_daily = len(user_stats) / user_stats['only_date'].nunique()
            UIComponents.create_metric_card(
                "Avg Messages/Day", 
                f"{avg_daily:.1f}"
            )
        
        with col3:
            most_active_hour = user_stats['hour'].mode().iloc[0] if not user_stats.empty else 0
            UIComponents.create_metric_card(
                "Most Active Hour", 
                f"{most_active_hour}:00"
            )

def show_text_analysis(df: pd.DataFrame, selected_user: str):
    """Display text analysis"""
    st.markdown("## Text Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        UIComponents.create_wordcloud_display(df_wc, "Most Common Words")
    
    with col2:
        st.markdown("### Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        UIComponents.create_bar_chart(
            pd.Series(most_common_df[1].values, index=most_common_df[0]),
            "Word Frequency",
            "#10B981"
        )
    
    # Emoji analysis
    st.markdown("### Emoji Analysis")
    emoji_df = helper.emoji_helper(selected_user, df)
    
    if not emoji_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top Emojis")
            st.dataframe(emoji_df.head(10), use_container_width=True)
        
        with col2:
            UIComponents.create_pie_chart(emoji_df.head(10), "Emoji Distribution")
    else:
        st.info("No emojis found in the selected chat data.")

def show_advanced_analysis(analyzer: AdvancedAnalyzer, selected_user: str):
    """Display advanced analysis features"""
    st.markdown("## Advanced Analysis")
    
    # Sentiment Analysis
    st.markdown("### Sentiment Analysis")
    sentiment_data = analyzer.sentiment_analysis(selected_user)
    
    if sentiment_data is not None and not sentiment_data.empty:
        UIComponents.create_sentiment_chart(sentiment_data)
        
        # Sentiment summary
        avg_sentiment = sentiment_data['avg_sentiment'].mean()
        sentiment_label = "Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            UIComponents.create_metric_card("Overall Sentiment", sentiment_label)
        with col2:
            UIComponents.create_metric_card("Avg Sentiment Score", f"{avg_sentiment:.3f}")
        with col3:
            UIComponents.create_metric_card("Analysis Period", f"{len(sentiment_data)} days")
    
    # Message Patterns
    st.markdown("### Message Patterns")
    patterns = analyzer.message_patterns(selected_user)
    
    if patterns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Hourly Activity")
            hourly_activity = patterns.get('hourly_activity', pd.Series())
            if not hourly_activity.empty:
                UIComponents.create_bar_chart(hourly_activity, "Messages by Hour", "#6366F1")
        
        with col2:
            st.markdown("#### Message Length Statistics")
            avg_length = patterns.get('avg_message_length', 0)
            UIComponents.create_metric_card("Average Message Length", f"{avg_length:.1f} characters")
    
    # Topic Modeling
    st.markdown("### Topic Analysis")
    topics = analyzer.topic_modeling(selected_user)
    
    if topics:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Most Common Words")
            top_words = topics.get('top_words', {})
            if top_words:
                words_df = pd.DataFrame(list(top_words.items()), columns=['Word', 'Count'])
                st.dataframe(words_df.head(10), use_container_width=True)
        
        with col2:
            st.markdown("#### Most Common Phrases")
            top_bigrams = topics.get('top_bigrams', {})
            if top_bigrams:
                bigrams_df = pd.DataFrame(list(top_bigrams.items()), columns=['Phrase', 'Count'])
                st.dataframe(bigrams_df.head(10), use_container_width=True)
    
    # Media Analysis
    st.markdown("### 📱 Media Analysis")
    media_analysis = analyzer.media_analysis(selected_user)
    
    if media_analysis:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            UIComponents.create_metric_card(
                "Total Media", 
                str(media_analysis.get('total_media', 0))
            )
        
        with col2:
            media_percentage = media_analysis.get('media_percentage', 0)
            UIComponents.create_metric_card(
                "Media Percentage", 
                f"{media_percentage:.1f}%"
            )
        
        with col3:
            if media_analysis.get('media_by_day'):
                most_active_day = max(media_analysis['media_by_day'], key=media_analysis['media_by_day'].get)
                UIComponents.create_metric_card(
                    "Most Active Day for Media", 
                    most_active_day
                )

if __name__ == "__main__":
    main() 