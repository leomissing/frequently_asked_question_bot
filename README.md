## Description

### Run with Python environment
In order for the bot to work, set the bot token, example is in [.env](.env). First step is setting environment variables:
```
export TG_BOT_TOKEN=*******
```

Build the bot:
```commandline
pip3 install -r requirements.txt
```
Testing the bot:
```commandline
pytest test.py
```

Running the bot:
```commandline
python run.py
```