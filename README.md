# USSD Mood Check

A USSD API for the Nalo Solutions gateway, built with Python and FastAPI.
When someone dials the USSD code, the gateway calls this API, which greets
the user and walks them through two menu screens.

**USSD code:** `*920*100#`

**Live endpoint:** `https://YOUR-APP.onrender.com/ussd`

## How it works

1. The user dials `*920*100#`.
2. Nalo sends a `POST` request with JSON to `/ussd`.
3. The API replies with JSON containing the text to show on the phone.
4. The user types a number, Nalo calls the API again, and the API replies with the next screen.

## Screens

**Screen 1** (first request):

```
Hello!
How are you feeling today?
1. Feeling fine
2. Feeling sad
3. Feeling frisky
```

**Screen 2** (depends on the choice, decided with `if / elif / else`):

| Input | Result |
|---|---|
| 1 | Feeling fine message, session ends |
| 2 | Relationship issues / Money problems / Family issues menu, session stays open |
| 3 | Feeling frisky message, session ends |
| anything else | Invalid choice message, session ends |

## Request and reply fields

Request from Nalo: `USERID`, `MSISDN`, `USERDATA`, `MSGTYPE`, `NETWORK`, `SESSIONID`.

Reply from this API: `USERID`, `MSISDN`, `MSG`, `MSGTYPE`.

- `MSGTYPE` in the request: `true` is the first request of a session, `false` is a follow-up.
- `MSGTYPE` in the reply: `true` keeps the session open, `false` ends it.
- If Nalo sends an empty `USERID`, the API falls back to the portal User ID.

## Limits

| Limit | Value | Source |
|---|---|---|
| Characters per screen (`MSG`) | 120 | Nalo API documentation, enforced in code |
| API response time | under 5 seconds | Project requirement |
| Session time limit | not yet confirmed | Not stated in the Nalo API document |

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Test with the requests in `test_main.http`, or with curl:

```bash
curl -X POST http://127.0.0.1:8000/ussd \
  -H "Content-Type: application/json" \
  -d '{"USERID":"","MSISDN":"233241234567","USERDATA":"*920*100#","MSGTYPE":true,"NETWORK":"MTN","SESSIONID":"abc123"}'
```

## Project files

- `main.py`: the API
- `requirements.txt`: Python dependencies
- `test_main.http`: sample requests for testing
- `README.md`: this file

## Known limitations

- Sessions are stored in the server's memory, so they are lost if the server restarts.
- Free hosting can put the server to sleep, which makes the first request slow.