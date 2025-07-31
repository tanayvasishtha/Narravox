# Narravox Setup Guide

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <your-repo-url>
   cd narravox
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   Create a `.env` file in the project root:
   ```
   PERPLEXITY_API_KEY=your_actual_perplexity_api_key
   QLOO_API_KEY=your_actual_qloo_api_key
   QLOO_BASE_URL=https://api.qloo.com/v1
   ```

3. **Run Locally**
   ```bash
   streamlit run app.py
   ```

## API Keys Required

### Perplexity Sonar API
- Get your API key from: https://www.perplexity.ai/pro
- Used for story generation and continuation
- Model: `perplexity/sonar-pro` (200,000 context window, advanced capabilities)

### Qloo Taste AI API
- Get your API key from: https://www.qloo.com/
- Used for cultural affinity enrichment
- Endpoints: `/affinities` and `/recommendations`

## Project Structure

```
narravox/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment config
├── .streamlit/
│   └── config.toml       # Swiss Design theme
├── api/
│   ├── perplexity_service.py  # LLM integration
│   └── qloo_service.py        # Cultural API integration
└── utils/
    ├── session_manager.py     # Session state management
    └── export_utils.py        # Story export functionality
```

## Features Implemented

✅ **Core Features**
- User input and story initiation
- Collaborative story building (15 turns max)
- Qloo cultural affinity enrichment
- Swiss Design interface (black/white/gray palette)

✅ **Advanced Features**
- Branching narrative options
- Cultural explanation overlays
- Story export (Text/PDF)
- Taste profile builder
- Demo mode with examples
- Error handling with retries

## Deployment on Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial Narravox implementation with all core features"
   git push origin main
   ```

2. **Deploy on Render**
   - Connect your GitHub repository
   - Render will automatically use `render.yaml`
   - Add environment variables in Render dashboard:
     - `PERPLEXITY_API_KEY`
     - `QLOO_API_KEY`

3. **Your app will be live at**: `https://narravox.onrender.com`

## Testing the Application

1. **Basic Test**
   - Start a story with: "A cyberpunk thriller with jazz influences"
   - Verify Qloo integration by checking Cultural Insights panel
   - Continue the story for a few turns

2. **Advanced Features Test**
   - Use "Get Options" to generate branching narratives
   - Try "Add Cultural Context" button
   - Export story as text or PDF
   - Test demo mode examples

## Architecture Highlights

- **Perplexity Sonar**: Handles all narrative generation and reasoning
- **Qloo Integration**: Provides cultural depth and cross-domain connections
- **Swiss Design**: Clean, minimalist interface following design principles
- **Session Management**: In-memory storage for simplicity and speed
- **Error Handling**: Comprehensive error management with user feedback

## Hackathon Submission Checklist

- [x] LLM Integration (Perplexity Sonar)
- [x] Qloo API Integration
- [x] Core functionality working
- [x] Advanced features implemented
- [x] Swiss Design principles applied
- [x] Deployment ready
- [x] Documentation complete
- [x] No emojis used anywhere in code/UI
- [x] Proper error handling
- [x] Export functionality

## Video Demo Script

1. **Intro (30s)**: Show clean Swiss Design interface
2. **Core Feature (60s)**: Create story with cultural enrichment
3. **Advanced Features (60s)**: Branching options, cultural insights
4. **Export Demo (30s)**: Download story as PDF
5. **Conclusion (30s)**: Highlight LLM + Qloo synergy

**Total Duration**: 3 minutes (perfect for submission) 