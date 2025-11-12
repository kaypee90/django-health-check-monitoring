# Contributing to Django Health Check Monitoring

Thank you for your interest in contributing to Django Health Check Monitoring! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Your environment (Python version, Django version, OS)
- Any relevant code samples or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

- A clear, descriptive title
- Detailed description of the proposed enhancement
- Examples of how it would be used
- Any potential drawbacks or considerations

### Pull Requests

1. **Fork the repository** and create your branch from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Set up your development environment**:
   ```bash
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/django-health-check-monitoring.git
   cd django-health-check-monitoring
   
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements/requirements_dev.txt
   ```

3. **Make your changes**:
   - Write clear, readable code
   - Follow PEP 8 style guidelines
   - Add or update tests as needed
   - Update documentation if you're changing functionality

4. **Run tests**:
   ```bash
   python manage.py test
   ```

5. **Run linting**:
   ```bash
   ruff check .
   ```

6. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference related issues (e.g., "Fixes #123")
   ```bash
   git commit -m "Add feature: description of feature"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```

8. **Create a Pull Request**:
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all tests pass
   - Wait for review and address any feedback

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Keep functions focused and concise
- Add docstrings to functions and classes
- Use type hints where appropriate

Example:

```python
def save_health_check_data_to_db(payload: dict) -> None:
    """
    Saves the health check data to the database.
    
    Args:
        payload: Dictionary containing health check data with 'checks' key
        
    Returns:
        None
    """
    logging.debug("saving health check data to database")
    # ... implementation
```

### Testing

- Write tests for new features and bug fixes
- Ensure all existing tests pass
- Aim for high test coverage
- Use descriptive test names

Example test structure:

```python
from django.test import TestCase
from django_health_check_job.models import HeathCheckJob

class HeathCheckJobModelTest(TestCase):
    def test_create_health_check_record(self):
        """Test that a health check record can be created"""
        record = HeathCheckJob.objects.create(
            name="TestCheck",
            status=1,
            message="working"
        )
        self.assertEqual(record.name, "TestCheck")
        self.assertEqual(record.status, 1)
```

### Documentation

- Update documentation for any user-facing changes
- Include docstrings in your code
- Update the README if needed
- Add examples for new features

### Commit Messages

Use clear, descriptive commit messages:

- **Good**: "Add support for custom health check intervals"
- **Good**: "Fix database connection leak in monitor command"
- **Bad**: "Update code"
- **Bad**: "Fix bug"

Format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic changes)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Project Structure

```
django-health-check-monitoring/
├── config/                      # Django project configuration
│   └── settings/               # Settings modules
├── django_health_check_job/    # Main app
│   ├── management/             # Management commands
│   │   └── commands/
│   │       └── monitor.py      # Monitor command
│   ├── migrations/             # Database migrations
│   ├── admin.py               # Admin configuration
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models
│   ├── tests.py               # Tests
│   ├── utils.py               # Utility functions
│   └── views.py               # Views (currently empty)
├── docs/                       # Documentation
├── requirements/               # Requirements files
├── manage.py                  # Django management script
├── setup.py                   # Package setup
└── README.rst                 # Project README
```

## Setting Up for Development

### Prerequisites

- Python 3.7 or higher
- pip
- virtualenv (recommended)
- Git

### Installation

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/django-health-check-monitoring.git
   cd django-health-check-monitoring
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements/requirements_dev.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Run tests to verify setup:
   ```bash
   python manage.py test
   ```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test django_health_check_job.tests.TestSpecificFeature

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Running Linters

```bash
# Check code with ruff
ruff check .

# Fix auto-fixable issues
ruff check . --fix
```

## Release Process

(For maintainers)

1. Update version in `setup.py` and `setup.cfg`
2. Update CHANGELOG.md
3. Create a git tag: `git tag -a v0.2.0 -m "Release version 0.2.0"`
4. Push tag: `git push origin v0.2.0`
5. Create GitHub release
6. Build and upload to PyPI:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## Getting Help

- Create an issue for bugs or feature requests
- Check existing issues and documentation
- Reach out to maintainers through GitHub

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in the project's README and release notes.

Thank you for contributing! 🎉
