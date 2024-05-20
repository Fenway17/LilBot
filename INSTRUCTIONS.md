**CREATING VIRTUAL ENVIRONMENT**
Go to your bot's working directory:
$ cd your-bot-source
$ python3 -m venv bot-env

Activate the virtual environment:
On Windows you activate it with:
$ bot-env\Scripts\activate.bat

Use pip like usual:
$ pip install -U discord.py

**CREATING REQUIREMENTS.TXT**
Activate your virtual environment
$ .\bot-env\Scripts\activate

Install the packages you need for your project using pip
$ pip install <PACKAGE_NAME>

Generate the requirements.txt file using pip freeze
$ pip freeze > requirements.txt

**INSTALLING REQUIREMENTS.TXT**
pip install -r requirements.txt

**RUNNING THE BOT**
py -3 src/main.py
