@echo off
echo Running Adeptly Tests with cleanup...
call venv\Scripts\activate.bat
python run_tests.py
pause
