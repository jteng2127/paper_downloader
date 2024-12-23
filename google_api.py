import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_credentials(
    token_file="token.json",
    credentials_file="credentials.json",
    scopes=SCOPES,
):
    """
    Gets valid user credentials.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds


def _get_max_list_length(values: list) -> int:
    max_length = 0
    for row in values:
        max_length = max(max_length, len(row))
    return max_length
    

def fetch_spreadsheet(creds, spreadsheet_id: str, range_name: str) -> pd.DataFrame:
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()
    result = (
        sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    )
    values = result.get("values", [])

    if not values:
        raise ValueError("No data found.")

    max_row_length = _get_max_list_length(values)
    for row in values:
        row += [""] * (max_row_length - len(row))

    df = pd.DataFrame(values[1:], columns=values[0])
    return df
