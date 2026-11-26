# USSD Mood Check API

A USSD Mood Check application built with **Python and FastAPI** and designed to work with the NALO Solutions USSD gateway.

The application allows users to select how they are feeling and then choose a reason for that feeling. It uses Python dictionaries, variables and session management to remember the user's selections throughout the USSD interaction.

## Project Overview

When a user dials the assigned USSD shortcode, NALO sends a request to this API. The application processes the user's input and returns the appropriate menu or response.

The application uses:

- Python
- FastAPI
- Pydantic
- Uvicorn
- In-memory session storage

## Live API

**Render endpoint:**

https://ussd-api-v0mr.onrender.com/ussd

**API documentation:**

https://ussd-api-v0mr.onrender.com/docs

## How It Works

The application has three stages.

### Screen 1: Feeling Selection

The user is presented with the following menu:

```text
How are you feeling today?
1. Feeling fine
2. Feeling sad
3. Feeling frisky
```

The user's selection is retrieved from the `feelings` dictionary.

### Screen 2: Reason Selection

After selecting a feeling, the application displays a follow-up menu.

For example, if the user selects Feeling sad:

```text
Why are you feeling sad?
1. Relationship issues
2. Money problems
3. Family issues
```

The same three reasons are available regardless of which feeling the user selects.

The selected feeling is stored in the user's session so that it can be retrieved on the next request.

### Screen 3: Final Response

After selecting a reason, the application retrieves both the feeling and reason from the appropriate variables and session.

For example:

```text
You are feeling sad because of family issues.
```

Other possible responses include:

```text
You are feeling fine because of money problems.
```

```text
You are feeling frisky because of relationship issues.
```

The final response is generated dynamically rather than using separate hardcoded messages for every possible combination.

## Session Management

The application uses a Python dictionary called `sessions` to store information about each USSD session.

Each session is identified using the NALO `SESSIONID`.

The selected feeling is saved and retrieved when the user makes their next selection.

This allows the application to remember the user's previous choice and use it to generate the final response.

## Request and Response Fields

### Incoming Request from NALO

| Field | Description |
|---|---|
| USERID | NALO account identifier |
| MSISDN | User's phone number |
| USERDATA | Value entered by the user |
| MSGTYPE | Indicates whether the request is the first request or a follow-up |
| NETWORK | User's mobile network |
| SESSIONID | Unique identifier for the USSD session |

### API Response

| Field | Description |
|---|---|
| USERID | NALO account identifier |
| MSISDN | User's phone number |
| MSG | Message displayed to the user |
| MSGTYPE | Indicates whether the USSD session should remain open or end |

### MSGTYPE Behaviour

- Request `MSGTYPE: true`: Indicates the first request of a USSD session.
- Request `MSGTYPE: false`: Indicates a follow-up request.
- Response `MSGTYPE: true`: Keeps the USSD session open.
- Response `MSGTYPE: false`: Ends the USSD session.

If NALO sends an empty `USERID`, the application uses the configured fallback User ID.

## Project Structure

```text
USSD-API/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

- `main.py`: Contains the FastAPI application, menus, session management and USSD logic.
- `requirements.txt`: Contains the Python dependencies.
- `README.md`: Project documentation.
- `.gitignore`: Specifies files and folders Git should ignore.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/ilamptey-rOvAk/ussd-api.git
```

### 2. Enter the project directory

```bash
cd ussd-api
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the FastAPI server

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## Testing the API

FastAPI provides an interactive documentation page for testing the endpoints.

Open:

```text
http://127.0.0.1:8000/docs
```

Find `POST /ussd` and use the **Try it out** option to send test requests.

Use the same `SESSIONID` throughout one USSD conversation to ensure the application retrieves the correct session information.

## Project Limitations

- Sessions are stored in server memory and are lost when the application restarts.
- The current in-memory session storage is not shared between multiple application workers.
- Free hosting may put the application to sleep, which can increase the response time of the first request after inactivity.
- The application limits outgoing USSD messages to 120 characters.

## Author

Developed as a Python FastAPI USSD integration project for the NALO Solutions gateway.