
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


# Main menu options
feelings = {
    "1": "Feeling fine",
    "2": "Feeling sad",
    "3": "Feeling frisky"
}


# Reason options
reasons = {
    "1": "Relationship issues",
    "2": "Money problems",
    "3": "Family issues"
}


# Store user sessions
sessions = {}


# USSD endpoint
@app.post("/ussd")
def ussd(req: NALORequest):

    log.info(f"IN: {req}")

    if req.MSGTYPE:

        msg = (
            "How are you feeling today?\n"
            "1. Feeling fine\n"
            "2. Feeling sad\n"
            "3. Feeling frisky"
        )

        keep_open = True

    else:

        choice = req.USERDATA.strip()
        session_id = req.SESSIONID

        # Check if the user already selected a feeling
        if session_id in sessions:

            selected_reason = reasons.get(choice)

            if selected_reason:

                # Retrieve the feeling stored in the session
                selected_feeling = sessions[session_id]["feeling"]

                # Combine the feeling and reason
                msg = (
                    f"You are {selected_feeling.lower()} "
                    f"because of {selected_reason.lower()}."
                )

                # Remove the session after the final response
                sessions.pop(session_id)

                keep_open = False

            else:

                # Display the reason menu again if the choice is invalid
                selected_feeling = sessions[session_id]["feeling"]

                msg = (
                    f"Why are you {selected_feeling.lower()}?\n"
                    "1. Relationship issues\n"
                    "2. Money problems\n"
                    "3. Family issues"
                )

                keep_open = True

        else:

            # Retrieve the feeling selected by the user
            selected_feeling = feelings.get(choice)

            if selected_feeling:

                # Store the selected feeling in the session
                sessions[session_id] = {
                    "stage": "reason_menu",
                    "feeling": selected_feeling
                }

                # Display the reason menu
                msg = (
                    f"Why are you {selected_feeling.lower()}?\n"
                    "1. Relationship issues\n"
                    "2. Money problems\n"
                    "3. Family issues"
                )

                keep_open = True

            else:

                # Invalid main menu selection
                msg = (
                    "Invalid choice. "
                    "Please select 1, 2 or 3."
                )

                keep_open = True

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
