#!/usr/bin/env python3
"""Setup script for Remote Check Meter development environment."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, check: bool = True) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{cmd}': {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up Remote Check Meter development environment...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install development dependencies
    print("\n📦 Installing development dependencies...")
    if not run_command("uv pip install -e '.[dev]'"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Install pre-commit hooks
    print("\n🪝 Installing pre-commit hooks...")
    if not run_command("pre-commit install"):
        print("❌ Failed to install pre-commit hooks")
        sys.exit(1)
    
    # Run initial formatting
    print("\n🎨 Running initial code formatting...")
    run_command("black src tests", check=False)
    run_command("isort src tests", check=False)
    
    # Run linting
    print("\n🔍 Running linting checks...")
    if not run_command("ruff check src tests", check=False):
        print("⚠️  Some linting issues found. Run 'make lint' to see details.")
    
    # Run tests
    print("\n🧪 Running tests...")
    if not run_command("pytest tests/ -v", check=False):
        print("⚠️  Some tests failed. Check test output above.")
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        print("\n📄 Creating .env file from template...")
        run_command("cp .env.example .env")
        print("✅ Created .env file. Please edit it with your credentials.")
    
    print("\n✅ Development environment setup complete!")
    print("\n📚 Next steps:")
    print("   1. Edit .env file with your credentials")
    print("   2. Run 'make help' to see available commands")
    print("   3. Run 'make check' to verify everything works")
    print("   4. Start developing! 🎉")


if __name__ == "__main__":
    main()