@echo off
setlocal
cd /d "%~dp0"
echo [1/4] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat
echo [2/4] Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [3/4] Preparing database...
python manage.py migrate
python manage.py seed_demo
echo [4/4] Starting MediCare Pharmacy...
echo Open http://127.0.0.1:8000/ and login with admin / admin123
python manage.py runserver
pause
