# Prerequisits:

python 3.12 and higher and poetry installed

### To start the repo

Run `poetry install`

Some endpoints require interaction with fetch.ai agent. We have included such `SampleAgent` in this repo. In order to start it(in a new terminal window), please navigate to the `SampleAgent` directory and run: `python sampleAgent.py`. On startup agent prints it's own address -> please include this address in `core/config.py`

cd into app directory and run `uvicorn main:app ` which starts the app with swagger interface on `http://0.0.0.0:8000/docs`.

### To run tests run this:

`poetry run pytest -s`

# If I forget to ask:

- atm the agent address is hardcoded in the `agentQuery`. Would it be better if the agent on startup would send it's address to the app or write it into a file from which we'd retrieve it?
