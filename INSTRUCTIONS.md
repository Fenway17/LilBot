# INSTRUCTIONS

**REQUIREMENTS**
Install and add FFmpeg to PATH

**NPM SCRIPTS**
Uses Node.js
Install NPM dependencies

- npm install

Setup virtual environment:

- npm run venv-setup

Optionally run format:

- npm run format-python

Activate the virtual environment:

- .\bot-env\Scripts\activate.bat

Install pip requirements

- npm run pip-install

Run bot:

- npm run dev

**CREATING VIRTUAL ENVIRONMENT**
Go to your bot's working directory:

- cd your-bot-source
- python3 -m venv bot-env

**CREATING REQUIREMENTS.TXT**
Activate your virtual environment

- .\bot-env\Scripts\activate

Install the packages you need for your project using pip

- pip install <PACKAGE_NAME>

Generate the requirements.txt file using pip freeze

- pip freeze > requirements.txt

**INSTALLING REQUIREMENTS.TXT**
Run it while inside the activated virtual environment

- pip install -r requirements.txt

**RUNNING THE BOT**
Run it while inside the activated virtual environment

- py -3 src/main.py
