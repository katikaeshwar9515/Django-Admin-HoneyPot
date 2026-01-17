# Quick Start Guide

## Local Development Setup

### Option 1: Using Setup Scripts (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Python (Cross-platform):**
```bash
python setup.py
```

### Option 2: Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration (defaults work for local development).

5. **Run migrations:**
   ```bash
   cd core
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Access the Application

- **Homepage:** http://127.0.0.1:8000
- **Fake Admin (Honeypot):** http://127.0.0.1:8000/admin/login
- **Real Admin:** http://127.0.0.1:8000/secret-admin-entrance/
- **API Swagger:** http://127.0.0.1:8000/swagger/

## Docker Setup

If you prefer using Docker:

```bash
docker compose up --build
```

## Important Notes

- The fake admin page (`/admin/`) is the honeypot - it will block IPs after failed login attempts
- The real admin is at `/secret-admin-entrance/`
- Default honeypot tryout limit is 3 (configurable in settings)
- If you get locked out, use Django shell to clear the blacklist:
  ```python
  from honeypot.models import BlackList
  BlackList.objects.all().delete()
  ```

