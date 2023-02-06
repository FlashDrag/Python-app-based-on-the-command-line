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
from pprint import pprint

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

    return result


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


def calculate_surplus_data(sales_row: list):
    '''
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
        - Positive surplus indicates waste
        - Negative surplus indicates extra made when stock was sold out.

    :param: list of integers
    '''
    print('Caclulating surplus data..\n')

    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def update_worksheet(data: list, worksheet: str):
    '''
    Receives a list of int to be inserted into a worksheet
    :param worksheet: worksheet name
    :param data: list of integers
    '''
    print(f'Updating {worksheet} worksheet..\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet.capitalize()} worksheet updated successfully.\n')


def get_last_5_entries_sales():
    '''
    Collects columns of data from sales worksheet, collecting
    the last 5 enteries for each sandwich and returns the data
    as a list of lists.
    '''
    sales = SHEET.worksheet('sales')

    columns = []
    for i in range(1, 7):
        column = sales.col_values(i)
        columns.append(column[-5:])

    return columns


def main():
    '''Run all program functions'''
    sales_data = get_sales_data()
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')

    sales_columns = get_last_5_entries_sales()


print('Welcome to Love Sandwiches Data Automation')
main()
