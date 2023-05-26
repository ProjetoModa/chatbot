# Chatbot

This is the backend used by the chatbot DigAI

## Install

Create the virtual environment, activate and install the required packages.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
#spacy download en_core_web_sm
```

Copy the .env and edit the necessary variables.

```bash
cp .env.example .env
```

Use the flask shell to create the database

```bash
flask shell
```

Inside the shell execute:

```python
from models import *
db.create_all()
```

## Execution

Use the flask program to start the development server

```bash
flask run
```
