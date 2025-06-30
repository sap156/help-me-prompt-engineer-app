# 🚀 Five Principles Prompt Engineering App

A comprehensive Python application that implements the **Five Principles of Prompting** to generate well-structured, optimized prompts for AI models. Available in both **Command Line** and **Beautiful Streamlit Web Interface** versions.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![LangChain](https://img.shields.io/badge/langchain-v0.1+-yellow.svg)

## 📖 About the Five Principles

This application is based on the proven **Five Principles of Prompting** methodology:

1. **🎯 Give Direction** - Provide clear, specific instructions and context
2. **📋 Specify Format** - Define the output structure and requirements  
3. **💡 Provide Examples** - Show what good output looks like
4. **✅ Evaluate Quality** - Set measurable criteria for success
5. **🔧 Divide Labor** - Break complex tasks into manageable steps

## ✨ Features

### 🌐 Streamlit Web App
- **Beautiful Interface** - Modern, responsive web design
- **Interactive Forms** - User-friendly input collection
- **Real-time Analytics** - Visual charts showing prompt quality metrics
- **Multiple Views** - Tabbed interface for results, breakdowns, and analysis
- **Copy & Download** - Easy export of generated prompts
- **Demo Mode** - Works without API keys for testing

### 💻 Command Line Version
- **Rich Console Interface** - Beautiful terminal experience with colors and progress bars
- **Guided Input** - Step-by-step prompts for all necessary information
- **File Export** - Save prompts to text files
- **Comprehensive Logging** - Detailed breakdown of each principle application

### 🤖 AI Integration
- **LangChain Framework** - Professional AI orchestration
- **OpenAI GPT Integration** - Powered by GPT-3.5-turbo
- **Smart Fallbacks** - Works in demo mode without API keys
- **Error Handling** - Graceful degradation when APIs are unavailable

## 🚀 Quick Start

### Option 1: Streamlit Web App (Recommended)

```bash
# Clone the repository
git clone https://github.com/sap156/help-me-prompt-engineer-app.git
cd help-me-prompt-engineer-app

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run prompt_app.py

# Open http://localhost:8501 in your browser
```

### Option 2: Command Line App

```bash
# Install dependencies
pip install -r requirements.txt

# Run in demo mode (no API key required)
python prompt_app.py --demo

# Run with OpenAI API
python prompt_app.py --api-key your_openai_key_here
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (optional - demo mode available)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sap156/help-me-prompt-engineer-app.git
   cd help-me-prompt-engineer-app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## 🔧 Usage

### Streamlit Web Interface

1. **Start the app:**
   ```bash
   streamlit run prompt_app.py
   ```

2. **Configure API** (or use Demo Mode):
   - Enter your OpenAI API key in the sidebar
   - Or toggle "Demo Mode" for testing without API

3. **Fill out the form:**
   - Describe your task
   - Specify audience, tone, format
   - Add any constraints
   - Set complexity level

4. **Generate and analyze:**
   - Click "Generate Optimized Prompt"
   - View results in multiple tabs
   - Copy or download your prompt

### Command Line Interface

```bash
# Interactive mode
python prompt_app.py

# With API key
python prompt_app.py --api-key sk-your-key-here

# Demo mode (no API required)
python prompt_app.py --demo

# Help
python prompt_app.py --help
```

## 📊 Example Output

The app transforms a simple request like:

**Input:** "Write a blog post about sustainable gardening"

**Into a comprehensive prompt:**

```
You are an expert assistant helping beginner gardeners. Your task is to write a blog post about sustainable gardening. Use a friendly and encouraging tone throughout your response. Context: Focus on urban environments with limited space.

Format your response as text. Keep it under 800 words and include 3 actionable tips.

Examples of good output:
- Example 1: [Sample blog post opening with encouraging tone]
- Example 2: [Example showing sustainable gardening tip format]  
- Example 3: [Example demonstrating urban gardening focus]

Quality criteria: Ensure your response directly addresses sustainable gardening, is appropriate for beginners, follows the text format exactly, maintains friendly tone.

Please approach this systematically:
1. Research sustainable gardening basics for beginners
2. Focus on urban environment solutions
3. Structure content with exactly 3 actionable tips
4. Review for friendly and encouraging tone

Now, please complete the task following all the above guidelines.
```

## 🎨 Screenshots

### Web Interface
![Streamlit Interface](screenshots/streamlit-main.png)
*Main input form with guided prompts*

![Results View](screenshots/streamlit-results.png)
*Tabbed results with analytics and breakdown*

### Command Line Interface
![CLI Interface](screenshots/cli-interface.png)
*Rich console interface with progress tracking*

## 🏗️ Project Structure

```
five-principles-prompt-engineering/
├── streamlit_app.py              # Main Streamlit web application
├── prompt_engineering_app.py     # Command line version
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── .env.example                  # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── LICENSE                      # MIT license
├── docs/                        # Documentation
│   ├── API.md                   # API documentation
│   ├── CONTRIBUTING.md          # Contribution guidelines
│   └── EXAMPLES.md              # Usage examples
├── tests/                       # Test files
│   ├── test_prompt_app.py       # Unit tests
│   └── test_streamlit_app.py    # Streamlit tests
├── screenshots/                 # Interface screenshots
├── examples/                    # Example prompts and outputs
│   ├── sample_prompts.md        # Sample generated prompts
│   └── use_cases.md            # Common use cases
└── scripts/                     # Utility scripts
    ├── setup.sh                 # Setup script
    └── deploy.sh               # Deployment script
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific tests
pytest tests/test_prompt_app.py
```

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=2000

# Streamlit Configuration
STREAMLIT_THEME_BASE=light
STREAMLIT_THEME_PRIMARY_COLOR=#1f77b4

# Application Settings
DEFAULT_COMPLEXITY=moderate
DEFAULT_FORMAT=text
ENABLE_ANALYTICS=true
```

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**
2. **Connect to Streamlit Cloud**
3. **Add secrets** in Streamlit Cloud dashboard:
   ```
   OPENAI_API_KEY = "your_api_key_here"
   ```
4. **Deploy automatically**

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_api_key_here

# Deploy
git push heroku main
```

### Deploy with Docker

```bash
# Build image
docker build -t prompt-engineering-app .

# Run container
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key prompt-engineering-app
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Development Setup

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```
4. **Make your changes**
5. **Run tests:**
   ```bash
   pytest
   ```
6. **Submit a pull request**

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)
- [Usage Examples](docs/EXAMPLES.md)
- [Five Principles Guide](docs/PRINCIPLES.md)

## 🐛 Troubleshooting

### Common Issues

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**OpenAI API errors:**
- Check your API key is valid
- Ensure you have credits available
- Try demo mode: `--demo` flag

**Streamlit won't start:**
```bash
streamlit --version
streamlit run streamlit_app.py --server.port 8501
```

**Permission errors:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## 📈 Roadmap

- [ ] **Multi-language support** - Support for prompts in different languages
- [ ] **More AI providers** - Integration with Claude, Gemini, etc.
- [ ] **Prompt templates** - Pre-built templates for common use cases
- [ ] **Team collaboration** - Shared workspaces and prompt libraries
- [ ] **API endpoint** - REST API for programmatic access
- [ ] **Mobile app** - React Native mobile version
- [ ] **Prompt analytics** - Advanced metrics and A/B testing
- [ ] **Enterprise features** - SSO, audit logs, advanced security

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT models
- **LangChain** for the excellent framework
- **Streamlit** for the beautiful web interface framework
- **The Prompt Engineering Community** for research and best practices

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/yourusername/five-principles-prompt-engineering/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/five-principles-prompt-engineering/discussions)
- **Email:** contact@yourproject.com

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/five-principles-prompt-engineering&type=Date)](https://star-history.com/#yourusername/five-principles-prompt-engineering&Date)

---

**Made with ❤️ by [Your Name](https://github.com/yourusername)**

*If you find this project helpful, please consider giving it a ⭐ star on GitHub!*