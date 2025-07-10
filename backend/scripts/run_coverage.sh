#!/usr/bin/env bash

# Exit immediately on error and show each command
set -e
set -x

# Optional: Clean previous coverage data
poetry run coverage erase

# Run tests with coverage collection (only for backend app code)
poetry run coverage run --source=backend -m pytest

# Print report in terminal, showing missing lines
poetry run coverage report --show-missing

# Generate HTML report with custom title (defaults to "Coverage Report" if none provided)
poetry run coverage html --title "${1:-Backend Coverage Report}"

# Optional: Open HTML report in default browser (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
  open htmlcov/index.html
fi
