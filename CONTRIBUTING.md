# 🤝 Contributing to AutoML Model Builder

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the AutoML Model Builder project.

## Code of Conduct

- Be respectful and inclusive
- Give credit where credit is due
- Focus on constructive feedback
- No harassment or discrimination
- Report violations to maintainers

## Getting Started

### 1. Set Up Development Environment

```bash
# Fork repository on GitHub
git clone https://github.com/yourusername/automl-model-builder.git
cd automl-model-builder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes

- Follow code style guidelines (see below)
- Write clear, descriptive commits
- Keep commits focused and atomic
- Add tests for new features

### 4. Test Your Changes

```bash
# Run tests
pytest tests/ -v

# Check code style
flake8 app/ ml/ --max-line-length=100
black --check app/ ml/

# Format code
black app/ ml/
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Descriptive title
- Detailed description of changes
- Reference to related issues
- Screenshots/demos if applicable

## Development Guidelines

### Code Style

**Python**
- Follow PEP 8
- Use 4 spaces for indentation
- Line length: 100 characters
- Use type hints (Python 3.10+)

```python
# Good
def validate_project_name(name: str) -> bool:
    """Validate project name format.
    
    Args:
        name: Project name to validate
        
    Returns:
        True if valid, False otherwise
    """
    return len(name) >= 1 and len(name) <= 100

# Bad
def validate_name(n):
    return len(n) >= 1 and len(n) <= 100
```

**JavaScript**
- Use ESLint configuration
- Use 2 spaces for indentation
- Const by default, let if needed, avoid var

```javascript
// Good
const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

// Bad
function validate_email(email) {
    return email.includes('@');
}
```

**CSS**
- Use CSS custom properties for colors
- Mobile-first responsive design
- Use semantic class names
- Group related rules together

```css
/* Good */
.btn-primary {
    background-color: var(--color-primary);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
}

/* Bad */
.btn {
    background-color: #3498db;
    padding: 10px;
    border-radius: 4px;
}
```

### Commit Messages

Format: `<type>: <subject>`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build, dependencies, etc.

**Examples:**
```
feat: add multi-step form wizard for model creation
fix: correct validation error message for file upload
docs: add deployment guide for Render
refactor: extract validation logic into utils
test: add tests for CSV validation
```

### Testing

Write tests for:
- All new features
- Bug fixes (test case that fails before fix)
- Edge cases
- Error conditions

```python
# Example test
import pytest
from app.utils.validation import validate_project_name

def test_validate_project_name_valid():
    assert validate_project_name("My Project") == True

def test_validate_project_name_empty():
    assert validate_project_name("") == False

def test_validate_project_name_too_long():
    assert validate_project_name("x" * 101) == False
```

### Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for structural changes
- Add docstrings to functions
- Comment complex logic
- Update CHANGELOG.md

```python
def calculate_accuracy(y_true, y_pred):
    """Calculate accuracy score.
    
    Accuracy is the ratio of correct predictions to total predictions.
    
    Args:
        y_true (array-like): True labels
        y_pred (array-like): Predicted labels
        
    Returns:
        float: Accuracy score (0-1)
        
    Example:
        >>> calculate_accuracy([1,0,1], [1,0,1])
        1.0
    """
    pass
```

## Areas to Contribute

### High Priority
- [ ] User authentication system
- [ ] Model versioning and comparison
- [ ] Real-time training progress tracking
- [ ] API endpoint improvements
- [ ] Database schema optimization

### Medium Priority
- [ ] Advanced hyperparameter tuning UI
- [ ] Model marketplace/sharing
- [ ] Collaborative projects
- [ ] Custom metric definitions
- [ ] Batch prediction API

### Low Priority
- [ ] UI/UX improvements
- [ ] Documentation translation
- [ ] Example projects
- [ ] Tutorial videos
- [ ] Community extensions

## Bug Reports

**Before reporting:**
- Search existing issues
- Test with latest code
- Gather system information

**Include:**
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/logs
- Environment details (OS, Python version, etc.)

**Example:**
```
Title: File upload fails for CSV > 10MB

Description:
When uploading a CSV file larger than 10MB, the upload fails.

Steps to reproduce:
1. Create CSV file > 10MB
2. Upload via form
3. See error

Expected: File uploads successfully (max 25MB supported)
Actual: Error message "File too large"

Environment:
- OS: macOS 13.2
- Python: 3.11.2
- Browser: Chrome 112
```

## Feature Requests

**Include:**
- Clear title and description
- Use case/motivation
- Proposed implementation (optional)
- Alternative approaches
- Related features

**Example:**
```
Title: Add real-time training progress display

Description:
Currently, users can't see training progress until completion.
This makes it hard to estimate completion time or debug issues.

Proposed solution:
Add WebSocket connection to display training metrics in real-time:
- Current epoch/batch
- Loss/accuracy graph
- Estimated time remaining
- Live log output

Benefits:
- Better UX
- Early issue detection
- User engagement
```

## Pull Request Process

### Checklist
- [ ] Code follows style guidelines
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
- [ ] No unrelated changes included

### Review Process

**Reviewers will check:**
1. Code quality and style
2. Test coverage
3. Documentation completeness
4. Security implications
5. Performance impact
6. Backward compatibility

**Feedback:**
- Request changes if needed
- Request review from maintainer if approved
- Author should update based on feedback

### Merging

- At least 1 approval required
- All checks must pass
- Squash commits (if preferred)
- Merge to main branch

## Development Workflow

### Local Development

```bash
# Start development server
python run.py

# In another terminal, watch CSS/JS
# (if setting up file watching)

# Access at http://localhost:5000
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_validation.py -v

# Run with coverage
pytest --cov=app --cov=ml tests/

# Run specific test
pytest tests/test_validation.py::test_validate_email -v
```

### Building Docker Image

```bash
# Build
docker build -t automl-builder:latest .

# Run
docker run -p 5000:5000 automl-builder:latest

# Test
curl http://localhost:5000/health
```

## Debugging

### Enable Debug Logging

```python
# In config.py or .env
LOG_LEVEL=DEBUG
FLASK_DEBUG=True
```

### Use Browser DevTools

**Chrome/Firefox:**
- F12 to open DevTools
- Console tab for JavaScript errors
- Network tab for API calls
- Application tab for local storage

### Debug Python Code

```python
# Add breakpoint
import pdb
pdb.set_trace()

# Or use VS Code debugger
# Set breakpoint and press F5
```

### Check Logs

```bash
# Follow log file
tail -f logs/automl.log

# Search logs
grep "ERROR" logs/automl.log

# Last N lines
tail -n 50 logs/automl.log
```

## Release Process

### Version Numbering

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Steps

1. Update version number
2. Update CHANGELOG.md
3. Create git tag
4. Push to main
5. Create GitHub release
6. Update documentation

```bash
# Create tag
git tag v1.2.0
git push origin v1.2.0
```

## Getting Help

- **Questions**: Use GitHub Discussions
- **Bugs**: Open GitHub Issue
- **Chat**: Join Discord community (if available)
- **Documentation**: See README.md and ARCHITECTURE.md

## Recognition

Contributors will be:
- Listed in README.md Contributors section
- Mentioned in release notes
- Credited in CHANGELOG.md

### Hall of Fame (10+ contributions)
- Added to project team
- GitHub star/recognition
- Potential maintainer status

## License

By contributing, you agree that your contributions will be licensed under the project's license (MIT).

## Questions?

Reach out to:
- **Issues**: For bugs and features
- **Discussions**: For questions
- **Email**: maintainer@example.com (if available)

---

**Thank you for contributing to make AutoML Model Builder better! 🎉**

Last Updated: May 2026
