# Contributing to Nurothon AI

First off, thank you for considering contributing to Nurothon AI! It's people like you that make this project a great tool for Indian SMBs.

## 🎯 Vision

Our goal is to make business automation accessible to every small business in India, regardless of technical expertise or language barriers.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** and description
- **Steps to reproduce** the behavior
- **Expected vs actual** behavior
- **Screenshots** if applicable
- **Environment details** (OS, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use case** - Why is this enhancement useful?
- **Proposed solution** - How should it work?
- **Alternatives considered** - What other solutions did you think about?

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message

## 💻 Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/nurothon-ai.git
cd nurothon-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v
```

## 📝 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Write tests for new features

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_ai_agent.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 📚 Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update API documentation if you add endpoints
- Create guides for new features

## 🌍 Internationalization

When adding new features:
- Support English, Hindi, and Hinglish
- Test with non-English inputs
- Use language-agnostic variable names

## 🎨 Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Example:
```
Add Hindi support for inventory queries

- Implement Hindi keyword matching
- Add test cases for Hindi inputs
- Update documentation

Fixes #123
```

## 📋 Pull Request Process

1. Update README.md with details of changes if needed
2. Update documentation for any new features
3. Add tests for new functionality
4. Ensure all tests pass
5. Request review from maintainers

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📞 Questions?

Feel free to create an issue or reach out to the maintainers.

Thank you for contributing! 🙏
