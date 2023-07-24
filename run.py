import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Corrected the line below to use 'scopes' instead of 'SCOPE'
CREDS = Credentials.from_service_account_file('creds.json', scopes=SCOPE)
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love-sandwiches')

# Renamed the 'sales' worksheet to 'sales_data' for clarity
sales_data = SHEET.worksheet('sales').get_all_values()

print(sales_data)

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
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data

def validate_data(values):
    """
    Check if exactly six values are entered.
    Check if these can be converted to integers
    """
    try:
        # Corrected the line below to convert each value to an integer
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
    update sales worksheet, add a new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully!.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print("Welcome to Love Sandwiches data automation!")
print("Welcome to Love Sandwiches data automation!")
main()