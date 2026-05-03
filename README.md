# 🚀 AEO Diagnostic Tool

A modern Answer Engine Optimization (AEO) diagnostic application built with Streamlit and Google's Gemini AI. This tool helps businesses evaluate how often and how well their products are recommended by AI engines compared to competitors, and provides actionable steps to improve AI visibility.

## ✨ Features

- **Visibility Scoring**: Calculates a percentage-based score of how often your product appears in top AI recommendations for a specific query.
- **Competitor Report Card**: Dynamically generates a report card (with grades A-F and AI Search Rank) and extracts exactly which top competitors are stealing your visibility.
- **AI Recommendations**: Fetches real-time product recommendations from the Gemini AI model.
- **Actionable Suggestions**: Automatically generates three actionable strategies to improve your product's naming, description, and positioning.
- **Interactive "How to Implement" Chat**: A follow-up chat interface where you can ask the AI for step-by-step implementation guides based on the provided suggestions.

## 🛠️ Tech Stack

- **Python 3.12**
- **Streamlit**: For the interactive web interface.
- **Google GenAI SDK (`google-genai`)**: To interact with the Gemini 2.5 Flash model.
- **python-dotenv**: For secure environment variable management.

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-github-repo-url>
cd aeo-tool
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: The `.env` file is included in `.gitignore` to keep your API keys secure.)*

### 5. Run the Application
```bash
streamlit run app.py
```

## 📂 Project Structure

- `app.py`: The main Streamlit frontend application, including state management and the chat interface.
- `llm_calls.py`: Handles all secure API interactions with the Google GenAI SDK.
- `prompts.py`: Contains the carefully crafted prompt templates for AEO evaluation.
- `analysis.py`: Contains the logic to parse AI responses and calculate visibility scores.
- `requirements.txt`: List of Python dependencies.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is open source and available under the [MIT License](LICENSE).
