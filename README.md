# Love Sandwiches

[Live link](https://love-sandwiches-code-inst.herokuapp.com/)

[SpreadSheet](https://docs.google.com/spreadsheets/d/1GLTH3nfhqOTAzVXfi88Qvox8sGyKK09mjTV5be8cv14/edit?usp=sharing)

This is a python script that uses the gspread library to access a Google Spreadsheet and perform operations on it. The script is used to manage the sales and stock data for a small business that sells sandwiches.

The program requests sales data from the user, validates it, and then updates three worksheets in the spreadsheet: sales, surplus, and stock. The sales worksheet is updated with the user's inputted data. The surplus worksheet is updated by comparing the user's inputted data (sales) with stock data from the spreadsheet and calculating the difference between them. Finally, the stock worksheet is updated by calculating an average of the last 5 entries in each column of sales data and adding 10%.

## Features
- Collects sales data from user input
- Validates the user's input and ensures that only 6 values are entered
- Updates the sales data in the 'sales' worksheet of the Google Spreadsheet
- Calculates the surplus data and updates it in the 'surplus' worksheet of the Google Spreadsheet
- Collects the last 5 sales entries for each item and calculates the average stock data
- Updates the average stock data in the 'stock' worksheet of the Google Spreadsheet

## Prerequisites
To run this script, you need to have the following installed:

- Python 3.x
- gspread library
- Google API credentials (in form of a JSON file)

## How to run
- Clone this repository to your local machine
- Replace the credentials JSON file with your own Google API credentials;

    [See instruction](instruction.md)
- Run the script by executing python run.py in the terminal
- Follow the prompts in the terminal to input the sales data
- The worksheets in the Google Spreadsheet will be updated with the sales, surplus, and stock data.

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Libraries used
- gspread: This is a Python library used to access and manage Google Spreadsheets.

- Google OAuth2 client: This is used to authenticate the application and grant it access to the Google APIs.


## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.
