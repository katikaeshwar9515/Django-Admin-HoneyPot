#!/bin/bash
# Setup script for Linux/Mac
echo "============================================================"
echo "Django HoneyPot Sample - Project Setup"
echo "============================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

echo "Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
    echo "Virtual environment created!"
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment and install requirements
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install requirements."
    exit 1
fi
echo "Dependencies installed!"

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Copying .env.example to .env..."
        cp .env.example .env
        echo "Please edit .env file with your configuration."
    else
        echo "Warning: .env.example not found. Please create .env manually."
    fi
fi

# Change to core directory and run migrations
cd core
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to run migrations."
    exit 1
fi
echo "Migrations completed!"

cd ..

echo ""
echo "============================================================"
echo "Setup completed successfully!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Run the server: python manage.py runserver"
echo ""
echo "Access the application at: http://127.0.0.1:8000"
echo "Fake admin (honeypot): http://127.0.0.1:8000/admin/login"
echo "Real admin: http://127.0.0.1:8000/secret-admin-entrance/"
echo ""

