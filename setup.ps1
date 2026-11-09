Set-Location $PSScriptRoot
Write-Host '[1/4] Creating virtual environment...'
py -m venv venv
& .\venv\Scripts\Activate.ps1
Write-Host '[2/4] Installing requirements...'
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host '[3/4] Preparing database...'
python manage.py migrate
python manage.py seed_demo
Write-Host '[4/4] Starting MediCare Pharmacy at http://127.0.0.1:8000/'
python manage.py runserver
