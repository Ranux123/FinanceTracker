import json
from datetime import datetime


# Global dictionary to store transactions
transactions = {}


# File handling functions
def load_transactions():
    global transactions #Assignning the global dictionary so it won't make new local scopes for every run of the program
    try:
        with open('db.json', 'r') as file:
            transactions = json.load(file) 
    except FileNotFoundError: #If file not found return an empty dictionary
        print("File Not Found.")
        transactions = {}
    except Exception as e: #Catch any other exceptions and return an empty dictionary as well
        print("An Error occured", (e))
        transactions = {} #Returns an empty dictionary.
    print(transactions)

def save_transactions():
    with open('db.json', 'w') as file: #Opening the file in write mode So that even if the file doesn't exist JSON file will  be created.
        json.dump(transactions, file, indent=2) #indent=2 for more readability and clear output in the JSON file.

def read_bulk_transactions_from_file(file_name):
    try:
        transactions_bulk = {} #Creatign a temporary dictionary to get the structure right.
        with open (file_name, 'r') as file_items: #Opening the file in read mode.
            for line in file_items: #Iterating over line by line the file has.
                transaction = line.strip().split(',') #strip to remove whitespaces while split to split the three values in the line using the comma.
                if len(transaction) == 3:
                    amount, category, date = transaction #Equaling the three values in the lines of the file to the dictionary three values.
                    amount = readbulk_amount(amount) #Checking whether the file contained amount values are acceptable for the program.
                    category = readbulk_category(category) #Checking whether the file contained category values are acceptable for the program.
                    date = readbulk_date(date) #Checking whether the file contained date values are acceptable for the program.

                    transaction_dict = {"amount": amount, "date": date} #Assignning the values we took from the file to the dictionary.
                    if category in transactions_bulk:
                        transactions_bulk[category].append(transaction_dict) #Appending to temporary dictionary before adding to the global dictionary for organizing.
                    else:
                        transactions_bulk[category] = [transaction_dict] #If the category is not already there then a category will be created and added to the dictionary.
                else:
                    print(f"Ignoring invalid transaction: {transaction}")


        for category, transactions_dict in transactions_bulk.items(): #Checking if the transaction already exists in the dicitonary and if it exists then skip those transactions and add the new ones. (Not duplicating is the purpose of this below code snippet)
            if category in transactions:
                existing_transactions = transactions[category]
                for new_transaction in transactions_dict:
                    if new_transaction not in existing_transactions:
                        existing_transactions.append(new_transaction)
            else:
                transactions[category] = transactions_dict
        save_transactions()
        print("Bulk transactions read successfully!")
        view_bulk_transactions(transactions_bulk)

    except FileNotFoundError:
        print("Such file not found!")

# Feature implementations
def add_transaction():
    global transactions
    transaction=[] #Declaring a list and inside them will be the transactions to each category in dictionary format.
    amount = validate_amount() #Validating whether the user input amount is acceptable by the program.
    category = validate_category() #Validating whether the user input category is acceptable by the program. 
    date = validate_date() #Validating whether the user input date is acceptable by the program.
    transaction_dict = {"amount": amount, "date": date}

    transaction.append(transaction_dict)

    if category in transactions:
        transactions[category].extend(transaction) #Extending the transaction if there is already a category exist by the same name.
    else:
        transactions[category] = transaction

    save_transactions()
    print("Transaction saved successfully!")


def view_transactions():
    global transactions
    if not transactions: #If there are no trasnactions an error message will be printed.
        transactions = {}
        print("No transactions to view!")
    else:
        for category, transaction_dict in transactions.items():
            print(f"{category}: ")
            for index, transaction in enumerate(transaction_dict, 1): #Getting the index of the transaction (Not the python actual index but the user friendly index)
                print(f"{index}. {transaction}\n")


def update_transaction():
    view_transactions()
    update_category = input("What Category do you want to Update: ").lower().capitalize() #Using the string serialization methods to make the user's life easier whatever the user types it will be converted inside the system to match with the system requirements.
    if update_category in transactions:
        transaction_dict = transactions[update_category]
        print(f"Category as requested ({update_category})")
        for index, transaction in enumerate(transaction_dict, 1):
            print(f"{index}. {transaction}")

        transaction_id = int(input("Enter the Transaction number that you need to Update: "))

        transaction_id = transaction_id - 1 #Substracting 1 assuming that the user doesn't have any idea about how python indexing handles.

        if 0 <= transaction_id < len(transaction_dict):
            amount = validate_amount() #Checking whether it's acceptable or not.
            date = validate_date() #Checking whther it's acceptable or not.

            transactions[update_category][transaction_id]["amount"] = amount
            transactions[update_category][transaction_id]["date"] = date

            save_transactions()
            print("Trasnaction updated successfully!")
        else:
            print("Invalid Trasnaction ID please enter a valid id.")
    else:
        print("No Trasnaction like that exists.")


def delete_transaction():
    view_transactions()
    delete_category = input("What Category do you want to Delete: ").lower().capitalize() #User's life get easier coz everything is handled by the backend user can enter whatever he wants.
    if delete_category in transactions:
        transaction_dict = transactions[delete_category]
        print(f"Category for deletion is {delete_category}")
        for index, transaction in enumerate(transaction_dict, 1):
            print(f"{index}. {transaction}")

        transaction_id = int(input("Enter the transaction number that you want to Delete: "))

        transaction_id = transaction_id - 1 #Substracting 1 assuming that the user doesn't have any idea about how python indexing works.

        if 0 <= transaction_id < len(transaction_dict): #Handling a bug identified via Testing.
            del transactions[delete_category][transaction_id] 

            if not transactions[delete_category]: #If there are no transactions in that category we are deleteing the category from the global dictionary as well for better strcture and better readability.
                del transactions[delete_category]

            save_transactions()
            print("Transaction deleted successfuly!")


def display_summary():
    if not transactions: #If there are no transactions to diplay a summary about then an error message will be diplayed.
        print("\nNo transactions to display summary.")
        return

    key_count = len(transactions.keys()) #Counting the number of transactions that got recorded for every transaction category.
    print(f"\nNo. of Transactions: {key_count}\n")

    print(" <- Summary ->\n") #Getting the sum of the each transactions happened in certain categories and displayign the sum of each transaction in every specific category.
    for category, transaction_list in transactions.items():
        total_amount = sum(transaction['amount'] for transaction in transaction_list)
        print(f"Transaction: {category}\t\t-\t{len(transaction_list)}\t\tTotal Amount:\tRs.{total_amount}")

def validate_amount():
    while True:
        try:
            amount = float(input("Enter the Amount :\t")) #Declared the amount as a float value coz there can be cents too.
            if amount <= 0: #Checking whether the input amount is a negative number.
                print("Please enter a value more than 0") #If it is prints this block.
            else:
                return amount #If not returns the amount
        except ValueError: #If the user didn't input a numeric value for the amount instead a string or something else then a valueError is raised and will print the below block.
            print("Please enter a valid numeric value for the amount.")

def readbulk_amount(amount):
    while True:
        try:
            amount = float(amount) #Converting the file amount to a float so that it matches with requirements of the program.
            if amount <= 0: #Checking if the amount is a negative number.
                print("Please enter a value more than 0")
            else:
                return amount
        except ValueError:
            print("Please enter a valid numeric value for the amount.")

def validate_category():
    while True:
        category = input("Enter the Category :\t").lower().capitalize() #Category is a string and used .lower() and .capitalize() for styling purposes.
        if category.isdigit(): #Checking if the transaction category is a numeric value if it is prints the below block.
            print("Category cannot be a numeric value. Please enter a description of the transaction.")
        else: #Else ask for an input again from the user.
            return category #Then returning the transaction category.
        
def readbulk_category(category):
    while True:
        category = category.lower().capitalize() #To convert the file categories so that it matches with the program requirements. 
        if category.isdigit():
            print("Category cannot be a numeric value. Please enter a description of the transaction.")
        else:
            return category
                    
def validate_date():
    while True:
        transaction_year = input("Enter the Year (YYYY->2024):\t") #Asking for the year
        transaction_month = input("Enter the Month (MM->04):\t") #Asking for the month
        transaction_day = input("Enter the Day (DD-04):\t") #Asking for the day
        date = f'{transaction_year}-{transaction_month}-{transaction_day}' #Interpret the year, month and day in the standard format by declaring a varible and using a f string.

        try: 
            datetime.strptime(date, "%Y-%m-%d") #Using datetime library i am checking if the user entered values are correct coz otherwise user can put 500 to date and month to 20 likewise. I am restricting that using this library.
            return date #If it's correct return transaction date.
        except ValueError: #If the user input a 500 to a day or 20 to a month a value error will be raised and if that happens the below block will be printed.
            print("Invalid date. Please enter the date in the asked format.")

def readbulk_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d") #Checking if the file dates are in the correct format if not printing an error message saying Invalid date.
        return date
    except ValueError:
        print("Invalid date. Please enter the date in the asked format.")

def view_bulk_transactions(transaction_bulk): #This function works only for the CLI. When the user adds the file to the dictionary this function is responsible for showing what are the transactions we are adding from the file to the dictionary.
    if not transaction_bulk:
        print("No transactions to view!")
    else:
        print("Bulk Transactions:")
        for category, transaction_list in transaction_bulk.items():
            print(f"{category}: ")
            for index, transaction in enumerate(transaction_list, 1): #Getting the index.
                print(f"{index}. {transaction}\n")

        
def main_menu():
    load_transactions()
    while True:
                print("\nPersonal Finance Tracker")
                print("1. Add Transaction")
                print("2. View Transactions")
                print("3. Update Transaction")
                print("4. Delete Transaction")
                print("5. Display Summary")
                print("6. Read from a file")
                print("7. Exit")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    add_transaction()
                elif choice == 2:
                    view_transactions()
                elif choice == 3:
                    update_transaction()
                elif choice == 4:
                    delete_transaction()
                elif choice == 5:
                    display_summary()
                elif choice == 6:
                    file = input("Enter the name of the file you want to open: ")
                    read_bulk_transactions_from_file(file)
                elif choice == 7:
                    print("Exiting the program!")
                    break
                if 0 < choice < 8:
                    pass 
                else:
                    print("Invalid choice!")

if __name__ == "__main__":
    main_menu()
