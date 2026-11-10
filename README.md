## Finance app

This app will alow you to manage your finances. Create spending / income categories, add expenses, add sources of income and get a good overview of how and where your finances are spent.


## Setup (dev)

- Make sure you have a postgres service running
- Copy `.env.example` to `.env` and set the correct settings
```bash
mv .env.example .env
```
- Make an environment, activate it and sync it
```bash
uv venv
source .venv/bin/activate
uv sync
```
- run the project by executing the following command:
```bash
uv run python manage.py runserver
```