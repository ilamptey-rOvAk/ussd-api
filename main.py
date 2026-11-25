from fastapi import FastAPI
from pydantic import BaseModel
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("ussd")
app = FastAPI()

@app.get("/")
def home():
    return {"Status": "USSD api is alive"}

class NALORequest(BaseModel):
    USERID: str = ""
    MSISDN: str = ""
    USERDATA: str = ""
    MSGTYPE: bool = True
    NETWORK: str = ""
    SESSIONID: str = ""

OPTIONS = (
    "How are you feeling today?\n"
    "1. Feeling fine\n"
    "2. Feeling sad\n"
    "3. Feeling frisky"
)
sessions = {}
@app.post("/ussd")
def ussd(req:NALORequest):
    log.info(f"IN: {req}")
    if req.MSGTYPE:
        msg = "Hello! AIK\n" + OPTIONS
        #msg = f"Hello {req.USERID}!\n" + OPTIONS
        # msg = f"Hello {req.MSISDN}!\n" + OPTIONS

        keep_open = True

    else:
        choice = req.USERDATA.strip()
        keep_open = False
        if sessions.get(req.SESSIONID) == "sad_menu":
            sessions.pop(req.SESSIONID)
            if choice == "1":
                msg = "Relationship issues:\nTalk it out with someone you trust."
            elif choice == "2":
                msg = "Money problems:\nMake a simple budget this week."
            elif choice == "3":
                msg = "Family issues:\nReach out to a family member you trust."
            else:
                msg = "Invalid choice.\nPlease dial again."
        elif choice == "1":
            msg = "Great to hear!\nKeep smiling and have a lovely day."
        elif choice == "2":
            msg = "Sorry to hear that.\n1. Relationship issues\n2. Money problems\n3. Family issues"
            keep_open = True
            sessions[req.SESSIONID] = "sad_menu"
        elif choice == "3":
            msg = "Ooh, frisky!\nEnjoy your day, stay safe."
        else:
            msg = "Invalid choice.\nPlease dial again and pick 1, 2 or 3."

    if len(msg) > 120:
        msg = msg[:120]

    reply = {
        "USERID": req.USERID or "AIK12356",
        "MSISDN": req.MSISDN,
        "MSG":msg,
        "MSGTYPE": keep_open,
    }
    log.info(f"OUT: {reply}")
    return reply