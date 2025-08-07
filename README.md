# 📱 WhatsApp Chat Analyzer

A comprehensive Streamlit application for analyzing WhatsApp chat exports with advanced features including sentiment analysis, user interaction patterns, and interactive visualizations.

## ✨ Features

### 📊 Basic Analysis
- **Message Statistics**: Total messages, words, media shared, and links
- **Timeline Analysis**: Monthly and daily message patterns
- **Activity Mapping**: Busy days, hours, and interactive heatmaps
- **User Analysis**: Most active users and interaction patterns

### 🎭 Advanced Features
- **Sentiment Analysis**: Analyze emotional tone of conversations
- **Message Patterns**: Response times, typing patterns, and message bursts
- **Topic Modeling**: Identify common themes and phrases
- **Media Analysis**: Media sharing patterns and trends
- **User Interaction Network**: Analyze conversation flows

### 🎨 Modern UI/UX
- **Interactive Charts**: Plotly-based visualizations
- **Tabbed Interface**: Organized analysis sections
- **Responsive Design**: Works on desktop and mobile
- **Error Handling**: Robust validation and error messages
- **Download Options**: Export analysis results

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd whatsapp-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app_enhanced.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📋 How to Use

### 1. Export WhatsApp Chat
- Open WhatsApp Web or mobile app
- Go to the chat you want to analyze
- Export chat (without media) as a .txt file
- Save the file to your computer

### 2. Upload and Analyze
- Use the file uploader in the sidebar
- Select your exported .txt file
- Choose analysis options (Overall or specific user)
- Click "Start Analysis"

### 3. Explore Results
- Navigate through different analysis tabs
- Interact with charts and visualizations
- Download results as CSV files
- Explore advanced features

## 🏗️ Project Structure

```
whatsapp-analysis/
├── app.py                 # Original application
├── app_enhanced.py        # Enhanced version with modern UI
├── helper.py              # Core analysis functions
├── preprocessor.py        # Data preprocessing
├── config.py              # Configuration settings
├── utils.py               # Utility functions and error handling
├── ui_components.py       # Modern UI components
├── advanced_analysis.py   # Advanced analysis features
├── requirements.txt       # Python dependencies
├── stop_hinglish.txt      # Stop words for text analysis
├── setup.sh              # Deployment configuration
└── README.md             # Project documentation
```

## 🔧 Configuration

The application uses a centralized configuration system in `config.py`:

- **Streamlit Settings**: Page title, icon, layout
- **Analysis Parameters**: Chart sizes, colors, limits
- **File Upload**: Size limits, allowed types
- **Chart Colors**: Consistent color scheme

## 🎯 Analysis Features

### Overview Tab
- Key statistics with modern cards
- Message and word counts
- Media and link analysis

### Timeline Tab
- Monthly and daily activity charts
- Interactive timeline visualizations
- Activity patterns by day and month

### User Analysis Tab
- Most active users ranking
- Individual user statistics
- User interaction patterns

### Text Analysis Tab
- Word cloud generation
- Most common words and phrases
- Emoji usage analysis

### Advanced Features Tab
- Sentiment analysis over time
- Message pattern analysis
- Topic modeling and bigram analysis
- Media sharing patterns

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **TextBlob**: Sentiment analysis
- **WordCloud**: Text visualization
- **NLTK**: Natural language processing

### Performance
- Optimized for large chat files
- Efficient data processing
- Caching for repeated analysis
- Memory management for large datasets

## 🚀 Deployment

### Local Development
```bash
streamlit run app_enhanced.py
```

### Cloud Deployment (Heroku)
1. Create a `Procfile`:
   ```
   web: streamlit run app_enhanced.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy using Heroku CLI:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app_enhanced.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- WhatsApp for chat export functionality
- Streamlit for the web framework
- Plotly for interactive visualizations
- TextBlob for sentiment analysis

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the documentation
- Review the code comments

---

**Made with ❤️ for WhatsApp chat analysis**

