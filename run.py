import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love-sandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)

def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers separated by commas.")
    print("Example: 23,45,34,67,89,2\n")

    data_str = input("Enter your data here: ")

    sales_data = data_str.split(",")
    validate_data(sales_data)

def validate_data(values):
    """
    Check if exactly six values are enterd.
    Check if these can be converted to ingers
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required and you provided only {len(values)}"
    
            )
    except ValueError as e:
        print(f"Invalid data {e}, please try again.\n")

get_sales_data()




