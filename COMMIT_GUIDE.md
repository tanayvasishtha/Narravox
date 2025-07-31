# Git Commit Guide for Narravox

## Initial Repository Setup

```bash
# Initialize repository
git init
git add .
git commit -m "Initial project structure and configuration"

# Create GitHub repository and connect
git remote add origin https://github.com/yourusername/narravox.git
git branch -M main
git push -u origin main
```

## Recommended Commit Sequence

### 1. Core Infrastructure
```bash
git add requirements.txt .streamlit/ render.yaml README.md
git commit -m "Added project dependencies and deployment configuration"
```

### 2. API Services
```bash
git add api/
git commit -m "Implemented Perplexity Sonar and Qloo API integration services"
```

### 3. Utilities and Session Management
```bash
git add utils/
git commit -m "Added session management and export utilities"
```

### 4. Main Application
```bash
git add app.py
git commit -m "Implemented main Streamlit application with Swiss Design interface"
```

### 5. Documentation
```bash
git add SETUP.md COMMIT_GUIDE.md
git commit -m "Added comprehensive setup and deployment documentation"
```

### 6. Final Push for Deployment
```bash
git add .
git commit -m "Final implementation ready for Qloo LLM Hackathon 2025 submission"
git push origin main
```

## Commit Message Guidelines

### Format
```
<type>: <description>

[optional body]
```

### Types
- `feat`: New feature implementation
- `fix`: Bug fixes
- `docs`: Documentation updates
- `style`: Code style changes (no functionality change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `deploy`: Deployment-related changes

### Examples of Good Commit Messages

✅ **Good Examples:**
```bash
git commit -m "feat: Add branching narrative options with Qloo cultural context"
git commit -m "fix: Handle API timeout errors with retry mechanism"
git commit -m "style: Apply Swiss Design principles to UI components"
git commit -m "docs: Add comprehensive setup guide for API configuration"
```

❌ **Avoid:**
```bash
git commit -m "updates"
git commit -m "fixed stuff"
git commit -m "work in progress"
```

## Branch Strategy

### Main Branch
- `main`: Production-ready code for deployment
- Always deployable to Render

### Development Workflow
```bash
# For new features (if needed)
git checkout -b feature/story-export
# ... make changes ...
git add .
git commit -m "feat: Implement PDF export functionality"
git checkout main
git merge feature/story-export
git push origin main
```

## Pre-Deployment Checklist

Before pushing to trigger Render deployment:

- [ ] All API integrations tested
- [ ] Swiss Design principles applied
- [ ] No emojis in code or UI
- [ ] Error handling implemented
- [ ] Documentation updated
- [ ] Requirements.txt current
- [ ] Environment variables documented

## Deployment Commands

```bash
# Final deployment commit
git add .
git commit -m "Deploy: Narravox v1.0 for Qloo LLM Hackathon 2025

- Complete Perplexity Sonar integration for story generation
- Full Qloo API integration for cultural enrichment
- Swiss Design interface with neutral color palette
- Advanced features: branching narratives, export, taste profiles
- Production-ready with comprehensive error handling"

git push origin main
```

## Render Auto-Deployment

Once pushed to GitHub:
1. Render detects changes automatically
2. Runs `pip install -r requirements.txt`
3. Starts app with `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. App available at: `https://narravox.onrender.com`

## Rollback Strategy

If deployment fails:
```bash
# Revert to last working commit
git log --oneline  # Find last working commit hash
git revert <commit-hash>
git push origin main
```

## Repository Best Practices

- Keep commits atomic (one logical change per commit)
- Write descriptive commit messages
- Update documentation with code changes
- Test locally before pushing
- Use meaningful branch names if using branches 