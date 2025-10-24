# 🤖 AI Tools Hub

A modern, full-stack web application that provides multiple AI-powered utilities in one place. Built with Flask, Transformers, and Bootstrap.

## ✨ Features

- 📝 **Text Summarizer**: Condense long articles using BART
- 🌍 **Language Translator**: Translate between multiple languages
- 💬 **Sentiment Analyzer**: Analyze emotional tone of text
- 🖼️ **Image Caption Generator**: Auto-generate image descriptions

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-tools-hub.git
cd ai-tools-hub
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

5. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. **Run the application**
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## 📁 Project Structure
```
ai-tools-hub/
├── app/
│   ├── __init__.py
│   ├── models/          # AI model classes
│   ├── routes/          # Flask blueprints
│   ├── static/          # CSS, JS, uploads
│   ├── templates/       # HTML templates
│   └── database.py      # Database models
├── config.py            # Configuration
├── run.py               # Entry point
└── requirements.txt     # Dependencies
```

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript/jQuery
- **AI/ML**: Transformers, PyTorch, NLTK, TextBlob
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Deployment**: Render, Railway, or Vercel

## 🌐 Deployment

### Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Use `render.yaml` configuration
5. Deploy!

### Deploy to Railway
```bash
railway login
railway init
railway up
```

### Deploy with Docker
```bash
docker-compose up --build
```

## 📊 API Endpoints

- `GET /` - Home page
- `POST /summarizer/api/summarize` - Summarize text
- `POST /translator/api/translate` - Translate text
- `POST /sentiment/api/analyze` - Analyze sentiment
- `POST /image-caption/api/caption` - Generate caption
- `GET /api/stats` - Usage statistics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Hugging Face for amazing Transformers library
- Flask community for excellent documentation
- Bootstrap team for beautiful UI components