# Contributing to Kohvilogi

Thank you for your interest in contributing! This document provides guidelines for setting up the project and submitting contributions.

## Development Setup

### Prerequisites

- Python 3.11+
- pip or uv package manager

### Installation

```bash
git clone https://github.com/stennu718/kohvilogi.git
cd kohvilogi
pip install -r requirements.txt
```

For development with test dependencies:

```bash
pip install -e ".[test]"
```

### Running the Development Server

```bash
uvicorn app.main:app --reload
```

The app will be available at `http://localhost:8000`.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test categories
pytest tests/ -v -m "not slow"       # Skip slow tests
pytest tests/ -v -m security          # Run security tests only
pytest tests/ -v -m e2e               # Run end-to-end tests only
```

## How to Contribute

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and ensure tests pass
5. **Commit** with a clear, descriptive message
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** against the `master` branch

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Ensure all tests pass before submitting
- Maintain test coverage above 80%
- Update documentation if your changes affect the API or user-facing behavior
- Write a clear PR description explaining the "what" and "why"

## Code Style

- **Language:** Python 3.11+
- **Style:** Follow PEP 8 conventions
- **Type hints:** Use type annotations for all function signatures
- **Async:** Use `async/await` for database and I/O operations
- **Naming:** Use descriptive variable and function names in English
- **Comments:** Add docstrings for public modules, classes, and functions
- **Testing:** Write tests for new features; use fixtures in `conftest.py` for common setup

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.
