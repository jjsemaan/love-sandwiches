import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Run while loop until correct data is input
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers separated by commas.")
        print("Example: 23,45,34,67,89,2\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data


def validate_data(values):
    """
    Check if exactly six values are enterd.
    Check if these can be converted to ingers
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required and you provided only {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data {e}, please try again.\n")
        return False
   
    return True

def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully!.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is calculated by subtracting sales figures from stock.
    -positive surplus indicates waste
    -negative surplus indicates extra sandwiches made when stocks run out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():
    """
    Run all program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("Welcome to love sanwiches data automation!")
main()