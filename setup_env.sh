#!/bin/bash
set -e

# Choose the venv directory (change as desired)
VENV_DIR=".venv"

echo "Creating Python virtual environment in $VENV_DIR..."
python3 -m venv $VENV_DIR

echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

if [ ! -f requirements.txt ]; then
  echo "ERROR: requirements.txt not found in current directory!"
  exit 1
fi

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate this environment later, run:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To deactivate, simply run:"
echo "  deactivate"
