@echo off
cd /d C:\Bots\bot_config_panel
start http://localhost:8000
python -m uvicorn app:app --reload
pause
