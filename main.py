
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


class NALORequest(BaseModel):
    USERID: str = ""
    MSISDN: str = ""
    USERDATA: str = ""
    MSGTYPE: bool = True
    NETWORK: str = ""
    SESSIONID: str = ""



feelings = {
    "1": "Feeling fine",
    "2": "Feeling sad",
    "3": "Feeling frisky"
}



reasons = {
    "1": "Relationship issues",
    "2": "Money problems",
    "3": "Family issues"
}



sessions = {}



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

    
        if session_id in sessions:

            selected_reason = reasons.get(choice)

            if selected_reason:

                
                selected_feeling = sessions[session_id]["feeling"]

                
                msg = (
                    f"You are {selected_feeling.lower()} "
                    f"because of {selected_reason.lower()}."
                )

                
                sessions.pop(session_id)

                keep_open = False

            else:

                
                selected_feeling = sessions[session_id]["feeling"]

                msg = (
                    f"Why are you {selected_feeling.lower()}?\n"
                    "1. Relationship issues\n"
                    "2. Money problems\n"
                    "3. Family issues"
                )

                keep_open = True

        else:

            
            selected_feeling = feelings.get(choice)

            if selected_feeling:

                
                sessions[session_id] = {
                    "stage": "reason_menu",
                    "feeling": selected_feeling
                }

                
                msg = (
                    f"Why are you {selected_feeling.lower()}?\n"
                    "1. Relationship issues\n"
                    "2. Money problems\n"
                    "3. Family issues"
                )

                keep_open = True

            else:

                
                msg = (
                    "Invalid choice. "
                    "Please select 1, 2 or 3."
                )

                keep_open = True

    
    if len(msg) > 120:
        msg = msg[:120]

    
    reply = {
        "USERID": req.USERID or "AIK12357",
        "MSISDN": req.MSISDN,
        "MSG": msg,
        "MSGTYPE": keep_open,
    }

    log.info(f"OUT: {reply}")

    return reply
