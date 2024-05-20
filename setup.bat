@echo off

REM Create virtual environment
python -m env bot-env

REM Activate virtual environment
call bot-env\Scripts\activate

REM Install dependencies
pip install -r requirements.txt