# 🚀 Five Principles Prompt Engineering App

A comprehensive Python web application that implements the **Five Principles of Prompting** to generate well-structured, optimized prompts for AI models. Built with **Streamlit** and **LangChain** for a beautiful, professional user experience.

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

### 🌐 Streamlit Web Interface
- **Beautiful UI** - Modern, responsive web design with custom styling
- **Interactive Forms** - Guided input collection with help text and validation
- **Real-time Analytics** - Visual charts showing prompt quality metrics
- **Multiple Views** - Tabbed interface for results, principle breakdown, and analysis
- **Copy & Download** - Easy export of generated prompts
- **Demo Mode** - Full functionality without requiring API keys

### 🤖 AI Integration
- **LangChain Framework** - Professional AI orchestration and chain management
- **OpenAI GPT Integration** - Powered by GPT-3.5-turbo for intelligent prompt generation
- **Smart Fallbacks** - Graceful degradation with demo mode when APIs are unavailable
- **Error Handling** - Robust error handling with user-friendly messages

### 📊 Analytics & Visualization
- **Confidence Scoring** - AI-generated confidence scores for prompt quality
- **Radar Charts** - Visual representation of principle implementation completeness
- **Word Count Analysis** - Bar charts showing content distribution across components
- **Progress Tracking** - Real-time feedback during prompt generation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (optional - demo mode available)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/five-principles-prompt-engineering.git
   cd five-principles-prompt-engineering
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

5. **Run the application:**
   ```bash
   streamlit run prompt_app.py
   ```

6. **Open your browser:**
   - Navigate to `http://localhost:8501`
   - Start generating optimized prompts!

## 🔧 Usage

### Web Interface

1. **Configure API Settings:**
   - Enter your OpenAI API key in the sidebar
   - Or enable "Demo Mode" for testing without API

2. **Describe Your Task:**
   - Enter what you want the AI to perform
   - Specify target audience and desired tone
   - Add any additional context

3. **Set Parameters:**
   - Choose output format (Text, JSON, Email, etc.)
   - Select task complexity level
   - Add specific constraints

4. **Generate Prompt:**
   - Click "Generate Optimized Prompt"
   - Watch the progress as each principle is applied
   - View results in multiple tabs

5. **Export Results:**
   - Copy prompt to clipboard
   - Download as text file
   - Analyze quality metrics

## 📊 Example Transformation

**Input:** "Write a blog post about sustainable gardening"

**Generated Optimized Prompt:**
```
You are an expert assistant helping beginner gardeners. Your task is to write a blog post about sustainable gardening. Use a friendly and encouraging tone throughout your response.

Format your response as Plain Text. Keep it under 800 words and include 3 actionable tips.

Examples of good output:
- Example 1: [Sample blog post opening with encouraging tone]
- Example 2: [Example showing sustainable gardening tip format]  
- Example 3: [Example demonstrating urban gardening focus]

Quality criteria:
Ensure your response: 1) Directly addresses sustainable gardening, 2) Is appropriate for beginner gardeners, 3) Follows the Plain Text format exactly, 4) Maintains friendly and encouraging tone

Approach this task step by step:
1. Analyze the write a blog post about sustainable gardening requirements
2. Research relevant information for beginner gardeners
3. Structure content in Plain Text format
4. Review and refine for friendly and encouraging tone

Now, please complete the task following all the above guidelines.
```

## 🏗️ Project Structure

```
five-principles-prompt-engineering/
├── prompt_app.py                 # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── LICENSE                      # MIT license
```

