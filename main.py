
from fastapi import FastAPI
from pydantic import BaseModel
import logging


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

log = logging.getLogger("ussd")

app = FastAPI()


# Home route
@app.get("/")
def home():
    return {"Status": "USSD api is alive"}


# NALO request structure
class NALORequest(BaseModel):
    USERID: str = ""
    MSISDN: str = ""
    USERDATA: str = ""
    MSGTYPE: bool = True
    NETWORK: str = ""
    SESSIONID: str = ""


# Welcome menu
OPTIONS = (
    "How are you feeling today?\n"
    "1. Feeling fine\n"
    "2. Feeling sad\n"
    "3. Feeling frisky"
)


# Store user sessions
sessions = {}


# USSD endpoint
@app.post("/ussd")
def ussd(req: NALORequest):

    log.info(f"IN: {req}")

    if req.MSGTYPE:
        msg = "Hello! AIK\n" + OPTIONS
        keep_open = True

    else:
        choice = req.USERDATA.strip()
        keep_open = False

        # User selected a reason after choosing Feeling sad
        if sessions.get(req.SESSIONID) == "sad_menu":

            sessions.pop(req.SESSIONID)

            if choice == "1":
                msg = (
                    "Relationships can be difficult sometimes. "
                    "Stay strong, communicate and remember that things can get better."
                )

            elif choice == "2":
                msg = (
                    "Financial challenges are temporary. "
                    "Stay focused, plan wisely and keep working towards better days."
                )

            elif choice == "3":
                msg = (
                    "Family challenges can be difficult. "
                    "Be patient, stay strong and never lose hope."
                )

            else:
                msg = "Invalid choice. Please dial again."

        # User selected Feeling fine
        elif choice == "1":

            msg = (
                "That's wonderful! Keep smiling, stay positive "
                "and have a beautiful day."
            )

        # User selected Feeling sad
        elif choice == "2":

            msg = (
                "Sorry to hear that.\n"
                "1. Relationship issues\n"
                "2. Money problems\n"
                "3. Family issues"
            )

            keep_open = True
            sessions[req.SESSIONID] = "sad_menu"

        # User selected Feeling frisky
        elif choice == "3":

            msg = "Ooh, frisky! Enjoy your day and stay safe."

        # Invalid selection
        else:

            msg = (
                "Invalid choice. "
                "Please dial again and pick 1, 2 or 3."
            )

    # Keep the response within 120 characters
    if len(msg) > 120:
        msg = msg[:120]

    # Response to NALO
    reply = {
        "USERID": req.USERID or "AIK12357",
        "MSISDN": req.MSISDN,
        "MSG": msg,
        "MSGTYPE": keep_open,
    }

    log.info(f"OUT: {reply}")

    return reply
