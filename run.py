"""
1. Create a spreadsheet with Google Sheets
2. Activate API credentials:
- Open Google Cloud Platform: https://console.cloud.google.com/
- Create `New Project`
- Select `APIs & Services` > `Library`
- Enable 2 APIs:
1) Google Drive API (enable)
- Generate credentials: `Create Credentials`
*API: Google Drive API
*Application data
*I'm not using this API with Compute Engine, Kubernetes Engine, App Engine, or Cloud Functions
*Service acc name and service acc ID - can be same as project name
*Role: Editor
- Load a file with credentials
*`APIs & Services` > `Credentials` > `Service Accounts` > select your acc
* In your service acc select `KEYS` > `ADD KEY` > `Create new Key` > `JSON`
2)Google Sheets
- Select `APIs & Services` > `Library` > `Google Sheets API` > Enable
3. Share access to Google sheets for service account
- Open your sheet in google and click `Share` green button
- Copy client email from downloaded credits json file and paste in sheet access:
* Make sure `Editor` is selected
* Untick `Notify People`
4. Move the json credentials file to repo and rename it to creds.json
* Hide the file, adding to .gitignore
5. Install:
 google auth - to set up the authentication needed to access the google cloud project
 gspread - library for acccesing and updating data in the spreadsheet
pip install --upgrade gspread google_auth
"""

import gspread
from google.oauth2.service_account import Credentials

# APIs list that the app should access in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open(
    "love_sandwiches"
)  # pass the name of the google spreadsheet


def get_sales_data() -> list:
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user via
    the terminal, which must be a string of 6 numbers separated by commas.
    The loop will repeatedly request data, until it is valid.
    :return: list of integers
    """

    print(
        "Enter sales data from the last market.\n"
        "Data should be six numbers, separated by comas.\n"
        "Example: 10,20,30,40,50,60\n"
    )
    while True:
        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")

        result = validate_data(sales_data)
        if result:
            break

    return sales_data


def validate_data(values: list) -> list:
    """
    Converts all string values into integers
    Raises error if there aren't 6 values or any string cannot be converted
    :param: list of strings
    :return: list of integers
    """

    try:
        if len(values) != 6:
            raise ValueError(f"Exactlty 6 values required, you provided {len(values)}.")
        result = [int(value) for value in values]
    except ValueError as e:
        print(e, "Try again.\n")
        return False
    else:
        return result


sales_data = get_sales_data()
