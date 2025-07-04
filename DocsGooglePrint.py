import os.path  # For checking if files exist and handling file paths

from google.auth.transport.requests import Request  # For refreshing OAuth2 credentials
from google.oauth2.credentials import Credentials  # For loading and saving OAuth2 credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # For handling OAuth2 user authorization flow
from googleapiclient.discovery import build  # For building the Google Docs API client
from googleapiclient.errors import HttpError  # For handling API errors

def extract_doc_id(url) -> str:
    """Extracts the document ID from a Google Docs URL."""
    import re
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    return match.group(1) if match else None

def return_TableContent(table) -> dict:
    """
    Extracts and organizes the content of a Google Docs table into a dictionary.
    Each row is mapped to a dictionary of its cell contents (up to 3 columns).
    """
    z = 0
    coordinates = {0: ""}
    for row in table.get("tableRows"):
        i = 0
        element = {0: "", 1: "", 2: ""}  # Prepare for up to 3 columns
        for cell in row.get("tableCells"):
            for content in cell.get("content"):
                paragraph = content.get("paragraph")
                for run in paragraph.get("elements"):
                    text_run = run.get("textRun")
                    if text_run:
                        contentCell = text_run.get("content").strip()
                        if z != 0 and i < 3:  # Skip header row, limit to 3 columns
                            element[i] = contentCell
                            i += 1
        if i > 0:
            coordinates[z] = element
        z += 1
    coordinates.pop(0, None)  # Remove the initial empty entry
    return coordinates

def print_UnicodeCaracter(x, y, char) -> None:
    """
    Prints a character at the specified (x, y) coordinates in the terminal using ANSI escape codes.
    """
    # ANSI escape code to move cursor: \033[<Y>;<X>H (1-indexed)
    print(f"\033[{y+1};{x+1}H{char}", end="")

def read_google_doc(doc_url) -> None:
    """
    Authenticates with Google, reads a Google Doc by URL, and prints table contents using coordinates.
    """
    # Extract the document ID from the URL
    doc_id = extract_doc_id(doc_url)

    # Define the required OAuth2 scope for read-only access to Google Docs
    SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

    if not doc_id:
        print("Invalid Google Doc URL.")
        return None

    creds = None
    # Check if token.json exists (stores user's access and refresh tokens)
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid credentials, start the OAuth2 flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh expired credentials
        else:
            # Start OAuth2 flow to get new credentials
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build the Google Docs API client
        service = build("docs", "v1", credentials=creds)

        # Retrieve the document's contents from the Docs service
        document = service.documents().get(documentId=doc_id).execute()
        # Iterate through the document's body content
        for element in document.get("body").get("content"):
            if "table" in element:
                # If the element is a table, extract and print its contents
                table = element.get("table")
                coordinatesDict = return_TableContent(table)
                qtdCoordinates = len(coordinatesDict)
                for coord in coordinatesDict:
                    element = coordinatesDict[coord]
                    # Print the character at the specified coordinates
                    print_UnicodeCaracter(int(element[0]), int(element[2]), element[1])

    except HttpError as err:
        print(err)

# Example usage: reads and prints table content from the specified Google Doc
read_google_doc("https://docs.google.com/document/d/1M0QY4-iKNHwPI3nS5LZBYDWXIpQzqypyzS_doHVHUEU/edit?tab=t.0")