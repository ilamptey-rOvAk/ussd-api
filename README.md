# USSD Mood Check

A USSD API for the Nalo Solutions gateway, built with Python and FastAPI.

USSD code: 920*100#

## Run locally
pip install -r requirements.txt
uvicorn main:app --reload

## How it works
Nalo sends a POST request to /ussd. The API greets the user and shows
a menu of three moods. The user's choice decides what screen 2 shows.
Sessions are kept in memory using SESSIONID.