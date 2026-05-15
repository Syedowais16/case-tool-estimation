# Contributing to CASE Tool

Thank you for your interest in contributing to the CASE Tool! This document provides guidelines and instructions for contributing.

## Code of Conduct

All contributors are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming environment

## Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/your-org/casetool.git
cd CaseTool
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bug-name
```

### 3. Set Up Development Environment
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Development Workflow

### Making Changes

1. **Code Style**: Follow PEP 8
   ```bash
   # Format code
   black app/

   # Lint code
   flake8 app/

   # Type check
   mypy app/
   ```

2. **Testing**: Write tests for new features
   ```bash
   # Run tests
   pytest -v

   # Check coverage
   pytest --cov=app tests/
   ```

3. **Commit Messages**: Follow conventional commits
   ```
   feat(auth): add two-factor authentication
   fix(estimate): correct COCOMO calculation
   docs(api): update endpoint documentation
   test(security): add JWT validation tests
   ```

### Commit Guidelines

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Limit to 50 characters for subject line
- Reference issues when relevant (#123)

## Pull Request Process

### Before Submitting PR

1. Update your branch with latest main
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. Run full test suite
   ```bash
   pytest --cov=app tests/
   ```

3. Check code style
   ```bash
   black --check app/
   flake8 app/
   ```

### PR Description

Include:
- What changes were made
- Why these changes are needed
- How the changes were tested
- Related issues (Fixes #123)
- Screenshots (if UI changes)

### Review Process

1. CI/CD checks must pass
2. Code review by maintainers
3. Address review comments
4. Final approval and merge

## Issues

### Reporting Bugs

Include:
- Python version
- PostgreSQL version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs

Example:
```
**Describe the bug**
Login fails with specific usernames

**Steps to reproduce**
1. Use email "test@example.com"
2. Enter password
3. Click login

**Expected behavior**
User should log in successfully

**Actual behavior**
Error: "Invalid credentials"

**Environment**
- Python 3.11.0
- PostgreSQL 15.1
- FastAPI 0.104.1
```

### Feature Requests

Include:
- Clear description
- Use case/motivation
- Proposed solution
- Alternative solutions

## Architecture Guidelines

### Backend

- **Layered Architecture**: Models → Schemas → Endpoints
- **Dependency Injection**: Use FastAPI dependencies
- **Error Handling**: Consistent exception handling
- **Validation**: Pydantic schemas for all inputs
- **Logging**: Structured logging throughout

### Frontend

- **Semantic HTML**: Proper element usage
- **CSS Organization**: Component-scoped styles
- **JavaScript**: ES6+, no external frameworks
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Optimize asset loading

## Testing Standards

### Unit Tests
- Test individual functions
- Mock external dependencies
- Aim for high coverage

### Integration Tests
- Test API endpoints
- Use test database
- Verify business logic

### Example Test
```python
def test_create_project(client, test_user, auth_headers):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Test Project",
            "budget": 50000,
            "team_size": 5
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
```

## Documentation

### Code Documentation
- Docstrings on all modules, classes, functions
- Type hints on all functions
- Comments for complex logic

### API Documentation
- Document all endpoints
- Include request/response examples
- Document error codes

### User Documentation
- Update README.md
- Update relevant guides
- Include examples

## Release Process

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create git tag
4. Update release notes
5. Deploy to production

## Helpful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Getting Help

- **Documentation**: See docs/ directory
- **Issues**: Search existing or create new
- **Email**: dev@casetool.example.com
- **Slack**: Join our development channel

## License

By contributing to CASE Tool, you agree that your contributions will be licensed under the Proprietary License.

## Questions?

Don't hesitate to ask! Open an issue with the `question` label.

---

Thank you for contributing to CASE Tool!
