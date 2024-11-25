import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
from tkinter import messagebox

#Global dictionary to store transactions
transactions = {}

#File handling functions
def load_transactions(filename):
    global transactions #Assigning the global dictionary so it won't make new local scopes whenever we run the program again and again.
    try:
        with open(filename, "r") as file:
            transactions = json.load(file)
        return transactions
    except FileNotFoundError: #If there is no such named file an empty dictionary will be returned.
        return {}

class FinanceTrackerGUI:
    def __init__(self, root): #init method
        self.root = root
        self.root.iconbitmap("icon.ico") #icon for the program
        self.root.title("Personal Finance Tracker") #title for the program
        self.create_widgets() #calling the create_widgets function so that every created widget using tkinter will be displayed.
        self.transactions = load_transactions("db.json")
        self.display_transactions(self.transactions)
        self.center_window() #when the GUI popup it is opened centered.

    def create_widgets(self):
        #Button Colors for styling purposes of the UI
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", background="blue", foreground="blue")

        self.style = ttk.Style()
        self.style.configure("Custom1.TButton", background="blue", foreground="blue")

        self.style = ttk.Style()
        self.style.configure("Custom2.TButton", background="black", foreground="black")

        # Frame for table and scrollbar
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying transactions (Table which contains transactions registered dividenly in three columns Category, Amount and Date)
        self.transaction_tree = ttk.Treeview(self.table_frame, columns=("Category", "Date", "Amount"))
        self.transaction_tree.heading("#0", text="Category")
        self.transaction_tree.heading("#1", text="Date")
        self.transaction_tree.heading("#2", text="Amount")
        self.transaction_tree.pack(side=tk.LEFT, expand=True, fill="both")  # Moved pack to left side

        # Making the scroll bar for transactions recorded which let the user experience easier.
        self.tree_scroll = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Search entry and button
        self.search_label = ttk.Label(self.root, text="Search a Transaction: ") #Label for searching
        self.search_label.pack(side=tk.LEFT, padx=(15, 5), pady=5)
        self.search_entry = ttk.Entry(self.root) #This is where the user enters the transaction amount, category or date.
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_button = ttk.Button(self.root, text="Search", command=self.search_transaction, style="Custom2.TButton") #Search Button
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        # BackButton for all the transactions from the search
        self.back_button = ttk.Button(self.root, text="Back", command=self.show_all_transactions, style="Custom2.TButton")
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5) #this button redirects you to all ht etransaction list after searching anything or sorting ascendingly or descendingly.

        # Widgets for Sorting Ascendingly or Discendingly.
        self.sort_by_category_asc_button = ttk.Button(self.root, text="Category (Asc)", command=lambda: self.sort_by_category('asc'), style="Custom.TButton") #This is for Category Ascending Sort
        self.sort_by_category_asc_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.sort_by_category_desc_button = ttk.Button(self.root, text="Category (Desc)", command=lambda: self.sort_by_category('desc'), style="Custom1.TButton") #This is for Category Descending Sort
        self.sort_by_category_desc_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.sort_by_amount_asc_button = ttk.Button(self.root, text="Amount (Asc)", command=lambda: self.sort_by_amount('asc'), style="Custom.TButton") #This is for Amount Ascending Sort
        self.sort_by_amount_asc_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.sort_by_amount_desc_button = ttk.Button(self.root, text="Amount (Desc)", command=lambda: self.sort_by_amount('desc'), style="Custom1.TButton") #This is for Amount Descending Sort
        self.sort_by_amount_desc_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.sort_by_date_asc_button = ttk.Button(self.root, text="Date (Asc)", command=lambda: self.sort_by_date('asc'), style="Custom.TButton") #This is for Date Ascending Sort
        self.sort_by_date_asc_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.sort_by_date_desc_button = ttk.Button(self.root, text="Date (Desc)", command=lambda: self.sort_by_date('desc'), style="Custom1.TButton") #This is for Date Descending Sort
        self.sort_by_date_desc_button.pack(side=tk.RIGHT, padx=5, pady=5)


    #This function is responsible for making the GUI pop up in the center of the screen
    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth() #This is getting width of the screen
        screen_height = self.root.winfo_screenheight() #This is getting height of the screen

        # Calculate the position of the window
        gui_screen_width = (screen_width - self.root.winfo_reqwidth()) // 2 #We are calculating the center by this line.
        gui_screen_height = (screen_height - self.root.winfo_reqheight()) // 2 #We are calculating the center by this line.

        # Set the position of the window
        self.root.geometry(f"+{gui_screen_width-410}+{gui_screen_height-80}") #Adjusting the position cordinates of the popped up GUI to pop from the dead center of the screen.

    #sorting by category in ascending and descending order
    def sort_by_category(self, order): #This function takes care of sorting the transactions by category asc and desc.
        sorted_transactions = sorted(self.transactions.items(), key=lambda x: x[0], reverse=order == 'desc')
        self.display_transactions(dict(sorted_transactions))

    #sorting by date in ascending and descending order
    def sort_by_date(self, order): #This function takes care of sorting the transactions by date asc and desc.
        sorted_transactions = sorted(self.transactions.items(), key=lambda x: min(t['date'] for t in x[1]), reverse=order == 'desc')
        self.display_transactions(dict(sorted_transactions))

    #sorting by amount in ascending and descending order
    def sort_by_amount(self, order): #This function takes care of sorting the trasnactions by amount asc and desc.
        sorted_transactions = sorted(self.transactions.items(), key=lambda x: sum(t['amount'] for t in x[1]), reverse=order == 'desc')
        self.display_transactions(dict(sorted_transactions))


    #Searching transactions by category name, date and amount
    def search_transaction(self):
        search_term = self.search_entry.get().lower()  # Get the search term from the entry widget
        if search_term: #If the search term is entered an empty dictionary will be created.
            matching_transactions = {}
            for category, transaction_list in self.transactions.items(): #Looping through the transactions
                matching_transactions[category] = []  #Creating a list for the searched transactions within the current category the function lopping through 
                for transaction in transaction_list:
                    if (search_term in category.lower() or  #Validates the category by making the user input value a lowercase string
                        search_term in str(transaction.get("date", "")).lower() or  # Validates the entered value matches with a date of a transaction
                        search_term in str(transaction.get("amount", "")).lower()):  # Validates the entered value matches with an amount of a transaction
                        matching_transactions[category].append(transaction) #If so appending that transaction to the list we created to the current loping category.

            # Check if any categories in matching_transactions have non-empty lists of transactions
            if any(matching_transactions.values()):
                self.display_transactions(matching_transactions) #Now if threre are matching transactions display them.
            else:
                messagebox.showinfo("No Matches", f"No transactions found for the search term '{search_term}'.") #If not a message box will appear.
        else:
            messagebox.showwarning("Empty Search", "Please enter a search term before searching.") #If there are no transactions entered in the search box a mesagebox will appear.



    #Dislaying all the transactions
    def show_all_transactions(self):
        self.display_transactions(self.transactions)

    #Displaying all the transactions and putting them into each section of category, amount and date.
    def display_transactions(self, transactions):
        # Clear existing entries in the treeview
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        # Add transactions to the treeview
        for category, transaction_list in transactions.items():
            for transaction in transaction_list:
                if isinstance(transaction, dict):
                    date = transaction.get("date", "")
                    amount = transaction.get("amount", "")

                    # Insert transaction into the treeview
                    self.transaction_tree.insert("", tk.END, text=category, values=(date, amount))

    def add_transaction(self, category, date, amount):
        if category in self.transactions:
            self.transactions[category].append({"amount": amount, "date": date}) #If three is already category named in the transaction then this will append. 
        else:
            self.transactions[category] = [{"amount": amount, "date": date}] #Otherwise it will create a new category and record the trasnaction there.

        self.display_transactions(self.transactions) #Updates the tkinter GUI with the newly recorded transaction
        save_transactions(self.transactions) #SAving the newly recorded transaction in the files.

    #Handling update transactions in the GUI
    def update_transaction(self, category, transaction_id, date, amount):
        if category in self.transactions: #Checking if the user entered category is in the trasnactions
            if 0 <= transaction_id < len(self.transactions[category]): #Validates the transaction id entered if it's usable by the program.
                self.transactions[category][transaction_id] = {"amount": amount, "date": date} #Updates the newly added values from the previous values.
                self.display_transactions(self.transactions) #Updates the GUI made via tkinter with the new updated values.
                save_transactions(self.transactions) #Saving the newly recorded values in the files.

    #Handling delete transactions in the GUI
    def delete_transaction(self, category, transaction_id):
        if category in self.transactions: #Checking if the user entered category is in the transactions 
            if 0 <= transaction_id < len(self.transactions[category]):
                del self.transactions[category][transaction_id] #Deleting hte transaction.
                if not self.transactions[category]:
                    del self.transactions[category]
                self.display_transactions(self.transactions) #Deleting that in the GUi as well.
                save_transactions(self.transactions) #SAving in the files.

#This function handles the saving of adding, updating or deleting transactions
def save_transactions(transactions):
    with open('db.json', 'w') as file:
        json.dump(transactions, file, indent=2)


def main_menu():
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
            add_transaction_cli()
        elif choice == 2:
            view_transactions()
        elif choice == 3:
            update_transaction_cli()
        elif choice == 4:
            delete_transaction_cli()
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


def add_transaction_cli():
    amount = validate_amount() #Validating whether the user input amount is acceptable by the program.
    category = validate_category() #Validating whether the user input category is acceptable by the program. 
    date = validate_date() #Validating whether the user input date is acceptable by the program.
    app.add_transaction(category, date, amount) #Appending


def update_transaction_cli():
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

            app.update_transaction(update_category, transaction_id, date, amount)
        else:
            print("Invalid Trasnaction ID please enter a valid id.")
    else:
        print("No Trasnaction like that exists.")


def delete_transaction_cli():
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
            app.delete_transaction(delete_category, transaction_id)
        else:
            print("Invalid Trasnaction ID please enter a valid id.")
    else:
        print("No Trasnaction like that exists.")


def view_transactions():
    global transactions
    if not transactions:
        transactions = {}
        print("No transactions to view!")
    else:
        for category, transaction_dict in transactions.items():
            print(f"{category}: ")
            for index, transaction in enumerate(transaction_dict, 1): #Getting the index..
                print(f"{index}. {transaction}\n")


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


def validate_category():
    while True:
        category = input("Enter the Category :\t").lower().capitalize() #Category is a string and used .lower() and .capitalize() for styling purposes.
        if category.isdigit(): #Checking if the transaction category is a numeric value if it is prints the below block.
            print("Category cannot be a numeric value. Please enter a description of the transaction.")
        else: #Else ask for an input again from the user.
            return category #Then returning the transaction category.


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


def read_bulk_transactions_from_file(file_name):
    try:
        transactions_bulk = {} #Creatign a temporary dictionary to get the structure right.
        with open (file_name, 'r') as file_items: #Opening the file in read mode.
            for line in file_items: #Iterating over line by line the file has.
                transaction = line.strip().split(',') #strip to remove leading and trailing whitespaces while split to split the three values in the line using the comma.
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

def view_bulk_transactions(transaction_bulk): #This function works only for the CLI. When the user adds the file to the dictionary this function is responsible for showing what are the transactions we are adding from the file to the dictionary.
    if not transaction_bulk:
        print("No transactions to view!")
    else:
        print("Bulk Transactions:")
        for category, transaction_list in transaction_bulk.items():
            print(f"{category}: ")
            for index, transaction in enumerate(transaction_list, 1): #Getting the index.
                print(f"{index}. {transaction}\n")


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


def readbulk_category(category):
    while True:
        category = category.lower().capitalize() #To convert the file categories so that it matches with the program requirements. 
        if category.isdigit():
            print("Category cannot be a numeric value. Please enter a description of the transaction.")
        else:
            return category


def readbulk_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d") #Checking if the file dates are in the correct format if not printing an error message saying Invalid date.
        return date
    except ValueError:
        print("Invalid date. Please enter the date in the asked format.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    main_menu()