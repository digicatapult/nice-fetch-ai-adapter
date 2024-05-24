# nice-fetch-ai-adapter

The purpose of this repository is to allow interaction between nice-agent-portal (PEER API), Veritable Peer and Cambridge's 'intelligent agent'.

### Endpoints

The endpoints in this repository are:
| endpoint |HTTP Methods| usage |
|----------|----|----------|
| "/send-query" |POST| Accepts query from Peer API, forwards it to Sample Agent & then to Veritable Peer. |
| "/webhooks/drpc"|POST| Accepts posts from veritable Cloudagent and passes them to PeerApi. These are either queries for peerApi or query responses for peer API. |
| "/receive-response" |POST| This endpoint receives information from chainvine and passes it to Veritable as a response. |

### Payload schemas:

#### POST/send-query schema inbound:

-> we only support method `query` for now

```
{
  "jsonrpc": "2.0",
  "method": "query",
  "params": [{<query json object>}],
  "id": "string"
}
```

#### POST/send-query schema outbound:

-> status 202 request received

#### POST/webhooks/drpc schema inbound:

- This schema can only include either `response` or `request`.
- If `request` is present, `role` must be `server` and if `response` is present `role` must be `client`

```
{
  "createdAt": "2024-05-23T08:23:49.183Z",
  "request": {
    "jsonrpc": "2.0",
    "method": "query",
    "params": [{<query json object>}],
    "id": "string"
  },
  "response": {
    "jsonrpc": "2.0",
    "result": {<response json object>},
    "error": {
      "code": -32601,
      "message": "string",
      "data": "string"
    },
    "id": <must match request.id>
  },
  "connectionId": "string",
  "role": "client" OR "server",
  "state": "request-sent",
  "threadId": "string",
  "id": "string"
}
```

#### POST/webhooks/drpc schema outbound:

-> status 202 request received

#### POST/receive-response schema inbound:

```
{
  jsonrpc: '2.0',
  result: {<response json object>},
  id: <must match request.id>
    "error": {
    "code": -32601,
    "message": "string",
    "data": "string"
  },
}

```

#### POST/receive-response schema outbound:

-> status 202 request received

### Prerequisites:

- python 3.12 or higher
- poetry installed

### To start the repo

Run `poetry install`

Some endpoints require interaction with fetch.ai agent. We have included such `SampleAgent` in this repo.
In order to bring up the repo run `python run.py` from your terminal (in root directory). This will bring up both the Sample fetch.ai agent and our app with swagger interface on `http://0.0.0.0:8000/docs`.
On startup agent prints it's own address -> please include this address in `core/config.py`(if it is different to the one hardcoded there).

### To run tests:

`poetry run pytest -s`
