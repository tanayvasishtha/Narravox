# Narravox

*Vocalize Worlds Woven from Cultural Affinities*

## Overview

Narravox transforms storytelling through the intelligent fusion of artificial intelligence and cultural understanding. This interactive platform enables users to collaborate with Perplexity Sonar's advanced language model while leveraging Qloo's sophisticated cultural intelligence API to create narratives that resonate with authentic cross-domain insights.

The application demonstrates how modern AI can transcend simple text generation by incorporating nuanced cultural affinities, connecting disparate elements like music preferences, travel destinations, and lifestyle brands into cohesive, compelling narratives.

## Architecture

### Core Technologies

**Language Model Integration**
- Perplexity Sonar Pro API (perplexity/sonar-pro)
- 200,000 context window with advanced capabilities
- Enhanced reasoning and double citations for narrative consistency
- Context-aware story continuation and branching

**Cultural Intelligence**
- Qloo Taste AI API for cross-domain affinity mapping
- Privacy-first entity extraction and recommendation
- Real-time cultural context enrichment

**Interface Design**
- Streamlit framework for rapid deployment
- Swiss Design principles throughout
- Responsive, accessibility-focused architecture

**Development Stack**
```
Python 3.9+
FastAPI for API orchestration
Streamlit for user interface
ReportLab for document generation
```

## Installation

### Prerequisites

Ensure Python 3.9 or higher is installed on your system.

### Quick Start

```bash
git clone https://github.com/yourusername/narravox.git
cd narravox
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```env
PERPLEXITY_API_KEY=your_perplexity_sonar_key
QLOO_API_KEY=your_qloo_api_key  
QLOO_BASE_URL=https://hackathon.api.qloo.com
```

### Local Development

```bash
streamlit run app.py
```

The application will be available at `chttp://localhost:8501`

## Features

### Story Generation Engine

**Collaborative Authoring**
Turn-based interaction between user and AI, maintaining narrative coherence across up to 15 exchanges while incorporating cultural context discovered through user input analysis.

**Cultural Context Discovery**
Automatic extraction of cultural entities from user input, with real-time querying of Qloo's API to discover cross-domain affinities that enrich narrative development.

**Branching Narratives**
AI-generated story path options that incorporate discovered cultural elements, allowing users to guide narrative direction while maintaining thematic consistency.

### User Experience

**Taste Profile Integration**
Optional pre-story profiling system that captures user preferences across multiple cultural domains, enabling more sophisticated cultural context generation.

**Swiss Design Interface**
Clean, minimal aesthetic using neutral color palette (white backgrounds, gray accents, black typography) with Helvetica-family fonts and grid-based layouts.

**Export Capabilities**
Story export in multiple formats including plain text and professionally formatted PDF documents, maintaining design consistency across all outputs.

### Technical Features

**Session Management**
Sophisticated state management preserving story history, cultural context, and user interactions throughout extended sessions.

**Error Handling**
Comprehensive error management with automatic retry logic for API failures and graceful degradation for partial service availability.

**Cultural Insights**
Expandable interface elements providing detailed explanations of discovered cultural connections and their relevance to the narrative.

## API Integration

### Perplexity Sonar

The application utilizes Perplexity's Sonar Pro model for sophisticated text generation with the following capabilities:

- Context-aware narrative generation
- Consistent character and plot development  
- Integration of cultural elements into storytelling
- Branching narrative option generation

### Qloo Taste AI

Cultural intelligence is provided through Qloo's comprehensive API:

- Entity extraction from natural language input
- Cross-domain affinity discovery
- Cultural recommendation generation
- Privacy-preserving taste profiling

## Deployment

## 🚀 Deployment

### Quick Deployment Check
Run the deployment script to verify everything is ready:
```bash
python deploy.py
```

### Render Deployment (Recommended)
1. Push your code to GitHub
2. Connect your repository to Render
3. Set environment variables in Render dashboard:
   - `PERPLEXITY_API_KEY` - Your Perplexity API key
   - `QLOO_API_KEY` - Your Qloo API key
   - `QLOO_BASE_URL=https://hackathon.api.qloo.com`
4. Deploy using the provided `render.yaml`

### Alternative Deployment Options

#### Heroku
```bash
heroku create narravox-app
heroku config:set PERPLEXITY_API_KEY=your_key
heroku config:set QLOO_API_KEY=your_key
git push heroku main
```

#### Railway
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically

#### Vercel
```bash
vercel --prod
```

### Environment Variables
Make sure to set these in your deployment platform:
- `PERPLEXITY_API_KEY` - Get from [Perplexity AI](https://www.perplexity.ai/settings/api)
- `QLOO_API_KEY` - Get from [Qloo Hackathon](https://hackathon.api.qloo.com)
- `QLOO_BASE_URL=https://hackathon.api.qloo.com`

### Production Configuration

The application is configured for deployment with the following specifications:

```yaml
services:
  - type: web
    name: narravox  
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### Continuous Deployment

Automatic deployment is configured through GitHub integration, with builds triggered on commits to the main branch.

## Usage Examples

### Basic Story Creation

1. Navigate to the application homepage
2. Enter a story prompt incorporating cultural elements
3. Click "Begin Story" to initiate AI generation
4. Continue the narrative through turn-based interaction

### Advanced Features

**Cultural Profiling**
Expand the "Build Taste Profile" section to input preferences across multiple cultural domains, enabling more sophisticated context generation.

**Branching Narratives**  
Use the "Get Options" button to generate AI-powered story continuation choices that incorporate discovered cultural affinities.

**Export and Sharing**
Access export functionality through the sidebar to generate formatted documents or shareable story links.

## Development

### Project Structure

```
narravox/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── render.yaml                # Deployment configuration
├── .streamlit/
│   └── config.toml            # Swiss Design theme configuration
├── api/
│   ├── perplexity_service.py  # LLM integration service
│   └── qloo_service.py        # Cultural AI integration service
└── utils/
    ├── session_manager.py     # State management utilities
    └── export_utils.py        # Document generation utilities
```

### Code Quality

The codebase adheres to professional development standards:

- Comprehensive error handling and logging
- Type hints throughout Python modules
- Clean architecture with separation of concerns
- Extensive documentation and inline comments

### Testing

Local testing can be performed using the integrated demo mode, which provides curated examples demonstrating all application features.

## Contributing

### Development Guidelines

- Follow Swiss Design principles in all interface modifications
- Maintain comprehensive error handling for all API interactions
- Ensure accessibility standards are met in all UI components
- Test thoroughly with both API services before submitting changes

### Code Style

- Use descriptive variable and function names
- Maintain consistent indentation and formatting
- Include docstrings for all public methods
- Follow PEP 8 guidelines for Python code

## License

This project is developed for the Qloo LLM Hackathon 2025. Please refer to the hackathon terms and conditions for usage guidelines.

## Support

For technical issues or questions regarding the application, please refer to the comprehensive setup documentation or create an issue in the project repository. 