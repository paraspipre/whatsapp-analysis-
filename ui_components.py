import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional
from config import CHART_COLORS, ANALYSIS_CONFIG

class UIComponents:
    """Modern UI components for the WhatsApp analyzer"""
    
    @staticmethod
    def create_header():
        """Create a modern header with title and description"""
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #1f77b4; font-size: 3rem; margin-bottom: 0.5rem;">
                WhatsApp Chat Analyzer
            </h1>
            <p style="color: #666; font-size: 1.2rem; margin-bottom: 2rem;">
                Discover insights from your WhatsApp conversations
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_sidebar():
        """Create an enhanced sidebar with file upload and user selection"""
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #1f77b4;">Analysis Controls</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # File upload section
            st.markdown("### Upload Chat File")
            uploaded_file = st.file_uploader(
                "Choose your WhatsApp chat export (.txt)",
                type=['txt'],
                help="Export your WhatsApp chat and upload the .txt file here"
            )
            
            if uploaded_file:
                st.success(f"File uploaded: {uploaded_file.name}")
                
                # File info
                file_size = uploaded_file.size / (1024 * 1024)  # MB
                st.info(f"File size: {file_size:.2f} MB")
            
            return uploaded_file
    
    @staticmethod
    def create_user_selector(user_list: List[str]) -> str:
        """Create a user selection dropdown"""
        st.markdown("### Select User")
        selected_user = st.selectbox(
            "Choose user for analysis:",
            user_list,
            help="Select 'Overall' to analyze the entire chat, or choose a specific user"
        )
        
        if selected_user == "Overall":
            st.info("Analyzing entire chat")
        else:
            st.info(f"Analyzing messages from: {selected_user}")
        
        return selected_user
    
    @staticmethod
    def create_stats_cards(stats: Dict[str, int]):
        """Create modern statistics cards"""
        st.markdown("## Key Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem;">{stats.get('messages', 0):,}</h3>
                <p style="margin: 0; opacity: 0.9;">Total Messages</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem;">{stats.get('words', 0):,}</h3>
                <p style="margin: 0; opacity: 0.9;">Total Words</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                        padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem;">{stats.get('links', 0):,}</h3>
                <p style="margin: 0; opacity: 0.9;">Links Shared</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_timeline_chart(timeline_data: pd.DataFrame, title: str = "Timeline"):
        """Create an interactive timeline chart using Plotly"""
        # Determine the x-axis column based on available columns
        if 'time' in timeline_data.columns:
            x_col = 'time'
            x_label = 'Time Period'
        elif 'only_date' in timeline_data.columns:
            x_col = 'only_date'
            x_label = 'Date'
        else:
            # Fallback to first column if neither exists
            x_col = timeline_data.columns[0]
            x_label = 'Time Period'
        
        fig = px.line(
            timeline_data, 
            x=x_col, 
            y='message',
            title=title,
            labels={x_col: x_label, 'message': 'Number of Messages'},
            line_shape='linear',
            render_mode='svg'
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            height=400,
            showlegend=False
        )
        
        fig.update_traces(
            line=dict(color=CHART_COLORS['primary'], width=3),
            marker=dict(size=6)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_activity_heatmap(heatmap_data: pd.DataFrame, title: str = "Activity Heatmap"):
        """Create an interactive activity heatmap"""
        fig = px.imshow(
            heatmap_data,
            title=title,
            aspect='auto',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_bar_chart(data: pd.Series, title: str, color: str = CHART_COLORS['primary']):
        """Create an interactive bar chart"""
        fig = px.bar(
            x=data.index,
            y=data.values,
            title=title,
            labels={'x': 'Category', 'y': 'Count'},
            color_discrete_sequence=[color]
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            height=400,
            showlegend=False
        )
        
        fig.update_traces(marker_line_color='white', marker_line_width=1.5)
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_pie_chart(data: pd.DataFrame, title: str = "Distribution"):
        """Create an interactive pie chart"""
        fig = px.pie(
            data,
            values=data.iloc[:, 1],
            names=data.iloc[:, 0],
            title=title
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_wordcloud_display(wordcloud_image, title: str = "Word Cloud"):
        """Display wordcloud with modern styling"""
        st.markdown(f"## {title}")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Use matplotlib to display wordcloud (same as original app)
            try:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.imshow(wordcloud_image, interpolation='bilinear')
                ax.axis('off')  # Hide axes
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)  # Close to free memory
            except Exception as e:
                st.error(f"Error displaying wordcloud: {str(e)}")
                st.info("WordCloud generation completed, but display failed.")
    
    @staticmethod
    def create_sentiment_chart(sentiment_data: pd.DataFrame):
        """Create sentiment analysis visualization"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Sentiment Over Time', 'Message Count Over Time'),
            vertical_spacing=0.1
        )
        
        # Sentiment line
        fig.add_trace(
            go.Scatter(
                x=sentiment_data['date'],
                y=sentiment_data['avg_sentiment'],
                mode='lines+markers',
                name='Sentiment',
                line=dict(color=CHART_COLORS['primary'])
            ),
            row=1, col=1
        )
        
        # Message count bar
        fig.add_trace(
            go.Bar(
                x=sentiment_data['date'],
                y=sentiment_data['message_count'],
                name='Messages',
                marker_color=CHART_COLORS['secondary']
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_tabs():
        """Create tabbed interface for different analysis sections"""
        return st.tabs([
            "Overview", 
            "Timeline", 
            "User Analysis", 
            "Text Analysis",
            "Advanced Features"
        ])
    
    @staticmethod
    def create_metric_card(title: str, value: str, delta: Optional[str] = None):
        """Create a metric card with optional delta"""
        if delta:
            st.metric(label=title, value=value, delta=delta)
        else:
            st.metric(label=title, value=value)
    
    @staticmethod
    def create_info_box(title: str, content: str, icon: str = ""):
        """Create an information box"""
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 10px; border-left: 4px solid #1f77b4;">
            <h4 style="margin: 0 0 0.5rem 0; color: #1f77b4;">{icon} {title}</h4>
            <p style="margin: 0; color: #666;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_download_button(data: pd.DataFrame, filename: str, button_text: str):
        """Create a download button for data"""
        csv = data.to_csv(index=False)
        st.download_button(
            label=button_text,
            data=csv,
            file_name=filename,
            mime='text/csv'
        ) 