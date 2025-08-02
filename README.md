# Remote Check Meter

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)

원격 검침 데이터를 가져와서 JSON 형식으로 변환하는 전문적인 Python 패키지입니다.

## 📁 Project Structure

```
remote-check-meter/
├── src/
│   └── remote_check_meter/          # Main package
│       ├── __init__.py              # Package entry point
│       ├── cli.py                   # Command line interface
│       ├── client.py                # Ruvie meter client
│       ├── config.py                # Configuration management
│       ├── parser.py                # Data parsing logic
│       ├── py.typed                 # Type hint marker
│       └── utils/                   # Utility modules
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_client.py
│   └── test_parser.py
├── scripts/                         # Scripts and utilities
│   ├── legacy/                      # Legacy implementation files
│   └── setup.py                     # Development setup script
├── data/                            # Data files (JSON, workflow)
├── pyproject.toml                   # Project configuration
├── Makefile                         # Development commands
└── README.md                        # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install with uv (recommended)
uv pip install -e .

# Install with development dependencies
uv pip install -e ".[dev]"

# Or use make command
make install-dev
```

### Basic Usage

```bash
# Using the CLI
remote-check-meter --help

# Specify year and month
remote-check-meter 2025 8

# With credentials
remote-check-meter --username myuser --password mypass 2025 8

# Multi-month query
remote-check-meter --multi 2025 8

# Save to file
remote-check-meter --output data.json 2025 8
```

### Python API

```python
from remote_check_meter import RuvieMeterClient
from remote_check_meter.config import load_config

# Load configuration
config = load_config()

# Create client and login
client = RuvieMeterClient()
client.login(config["username"], config["password"])

# Fetch meter data
data = client.fetch_meter_data(2025, 8)
print(data)
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and setup
git clone <repository-url>
cd remote-check-meter
make setup-dev
```

### Available Commands

```bash
make help                # Show all available commands
make install            # Install project dependencies
make install-dev        # Install with dev dependencies
make setup-dev          # Setup complete dev environment
make format             # Format code with black and isort
make lint               # Run all linting checks
make test               # Run tests
make test-cov           # Run tests with coverage
make check              # Run format, lint, and test
make clean              # Clean build artifacts
make build              # Build the package
```

### Code Quality Tools

This project uses modern Python development tools:

- **[Black](https://black.readthedocs.io/)**: Code formatting
- **[isort](https://pycqa.github.io/isort/)**: Import sorting
- **[Ruff](https://docs.astral.sh/ruff/)**: Fast linting and code analysis
- **[MyPy](https://mypy.readthedocs.io/)**: Static type checking
- **[pytest](https://docs.pytest.org/)**: Testing framework
- **[pre-commit](https://pre-commit.com/)**: Git hooks for code quality

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
make pre-commit
```

## 📊 Output Format

```json
{
  "year": 2025,
  "month": 8,
  "total_records": 31,
  "data": [
    {
      "date": "2025-08-02",
      "cumulative_usage_kwh": 37132.6,
      "daily_usage_kwh": 2.7,
      "timestamp": "2025-08-02T00:00:00"
    },
    {
      "date": "2025-08-01",
      "cumulative_usage_kwh": 37129.9,
      "daily_usage_kwh": 32.6,
      "timestamp": "2025-08-01T00:00:00"
    }
  ],
  "summary": {
    "total_usage_kwh": 1234.5,
    "average_daily_usage_kwh": 39.8,
    "peak_usage_kwh": 65.2,
    "peak_usage_date": "2025-08-15"
  }
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Ruvie login credentials
RUVIE_USERNAME=your_username
RUVIE_PASSWORD=your_password

# Optional settings
RUVIE_BASE_URL=https://www.ruvie.co.kr
METER_BASE_URL=http://14.33.118.151
DEBUG=false
```

### Configuration File

Alternatively, use a JSON configuration file:

```json
{
  "username": "your_username", 
  "password": "your_password",
  "base_url": "https://www.ruvie.co.kr",
  "meter_base_url": "http://14.33.118.151",
  "timeout": 30,
  "retries": 3
}
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test
pytest tests/test_client.py -v

# Run tests with markers
pytest -m "not slow" tests/
```

## 📈 Type Checking

This package includes complete type annotations:

```bash
# Run mypy type checking
make lint

# Or directly
mypy src/
```

## 🔒 Security Notes

- **Credentials**: Store login credentials securely using environment variables or configuration files
- **SSL**: SSL certificate verification is disabled for the meter endpoint - use caution in production
- **Dependencies**: Regular security updates for all dependencies via `pip-audit`

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver**: For Selenium-based legacy scripts, ensure ChromeDriver is installed:
   ```bash
   # macOS
   brew install chromedriver
   
   # Linux 
   sudo apt-get install chromium-chromedriver
   ```

2. **SSL Issues**: If you encounter SSL certificate errors, verify the meter endpoint configuration

3. **Login Issues**: Check credentials and ensure the Ruvie website is accessible

### Debug Mode

Enable debug logging:

```bash
export DEBUG=true
remote-check-meter --year 2025 --month 8
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run quality checks: `make check`
5. Commit changes: `git commit -m "Add feature"`
6. Push to branch: `git push origin feature-name`
7. Create a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines (enforced by Black and Ruff)
- Add type hints for all new code
- Write tests for new functionality
- Update documentation for API changes
- Run `make check` before committing