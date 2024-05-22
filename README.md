# nice-fetch-ai-adapter

The purpose of this repository is to allow interaction between nice-agent-portal (PEER API), Veritable Peer and Cmbridge's 'intelligent agent'.
The endpoints in this repository are:
| endpoint | usage |
|----------|----------|
| "/send-query" | Accepts query from Peer API, forwards it to Sample Agent & then to Veritable Peer. |
| "/webhooks/drpc"| Accepts posts from veritable Cloudagent and passes them to PeerApi. These are either queries for peerApi or query responses for peer API. |
| "/receive-response" | This endpoint receives information from chainvine and passes it to Veritable as a response. |

### Prerequisites:

- python 3.12 or higher
- poetry installed

### To start the repo

Run `poetry install`

Some endpoints require interaction with fetch.ai agent. We have included such `SampleAgent` in this repo. In order to start it (in a new terminal window), please navigate to the `SampleAgent` directory and run: `python sampleAgent.py`. On startup agent prints it's own address -> please include this address in `core/config.py`

Open new terminal window, cd into app directory and run `uvicorn main:app ` which starts the app with swagger interface on `http://0.0.0.0:8000/docs`.

### To run tests:

`poetry run pytest -s`
