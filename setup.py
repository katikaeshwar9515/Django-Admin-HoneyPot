"""
Setup script for Django HoneyPot Sample Project
Run this script to set up the project for local development.
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0

def main():
    """Main setup function."""
    print("=" * 60)
    print("Django HoneyPot Sample - Project Setup")
    print("=" * 60)
    
    # Check if Python is available
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Change to core directory
    core_dir = Path("core")
    if not core_dir.exists():
        print("Error: 'core' directory not found. Please run this script from the project root.")
        sys.exit(1)
    
    os.chdir(core_dir)
    print(f"Changed to directory: {os.getcwd()}")
    
    # Check if virtual environment exists
    venv_path = Path("../venv")
    if not venv_path.exists():
        print("\nCreating virtual environment...")
        if not run_command(f"{sys.executable} -m venv ../venv"):
            print("Error: Failed to create virtual environment.")
            sys.exit(1)
        print("Virtual environment created successfully!")
    else:
        print("\nVirtual environment already exists.")
    
    # Determine activation script based on OS
    if sys.platform == "win32":
        activate_script = "../venv/Scripts/activate"
        python_exe = "../venv/Scripts/python.exe"
        pip_exe = "../venv/Scripts/pip.exe"
    else:
        activate_script = "../venv/bin/activate"
        python_exe = "../venv/bin/python"
        pip_exe = "../venv/bin/pip"
    
    # Install requirements
    print("\nInstalling dependencies...")
    requirements_path = Path("../requirements.txt")
    if requirements_path.exists():
        if not run_command(f"{pip_exe} install --upgrade pip"):
            print("Warning: Failed to upgrade pip, continuing anyway...")
        
        if not run_command(f"{pip_exe} install -r ../requirements.txt"):
            print("Error: Failed to install requirements.")
            sys.exit(1)
        print("Dependencies installed successfully!")
    else:
        print("Warning: requirements.txt not found.")
    
    # Check for .env file
    env_path = Path("../.env")
    env_example_path = Path("../.env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            print("\n.env file not found. Copying from .env.example...")
            import shutil
            shutil.copy(env_example_path, env_path)
            print("Please edit .env file with your configuration.")
        else:
            print("\nWarning: .env file not found. Please create one manually.")
    
    # Run migrations
    print("\nRunning database migrations...")
    if not run_command(f"{python_exe} manage.py makemigrations"):
        print("Warning: makemigrations had issues, continuing...")
    
    if not run_command(f"{python_exe} manage.py migrate"):
        print("Error: Failed to run migrations.")
        sys.exit(1)
    print("Migrations completed successfully!")
    
    # Create superuser prompt
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print(f"1. Activate virtual environment:")
    if sys.platform == "win32":
        print(f"   .\\venv\\Scripts\\activate")
    else:
        print(f"   source venv/bin/activate")
    print(f"2. Create a superuser (optional):")
    print(f"   python manage.py createsuperuser")
    print(f"3. Run the development server:")
    print(f"   python manage.py runserver")
    print(f"\nAccess the application at: http://127.0.0.1:8000")
    print(f"Fake admin (honeypot): http://127.0.0.1:8000/admin/login")
    print(f"Real admin: http://127.0.0.1:8000/secret-admin-entrance/")

if __name__ == "__main__":
    main()

