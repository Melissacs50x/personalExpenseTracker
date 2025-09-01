import db
from datetime import datetime
import csv
import GUI

# Initialize the database
db.init_db()

# ----------------- Menu Display -----------------

def show_menu():
    print(
        "1) Add transaction\n"
        "2) Show all transactions\n"
        "3) Show balance\n"
        "4) Show by (date/category)\n"
        "5) Edit transaction\n"
        "6) Delete transaction\n"
        "7) Export to CSV\n"
        "8) Generate report\n"
        "9) Show chart\n"
        "10) Exit"
    )

# ----------------- Add New Transaction -----------------

def add_transaction():
    amount = float(input("Amount: "))
    type = input("Type: ")
    category = input("Category: ")
    note = input("Note: ")
    date = input("Enter date (yyyy-mm-dd) or leave empty for today: ").strip()
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    db.save_transaction(amount, type, category, note, date)

# ----------------- Show All Transactions -----------------

def show_transactions():
    result = db.show_transaction()
    if not result:
        print("No transactions found!")
    else:
        for tran in result:
            print(f'{tran[0]}) Amount: {tran[1]}, Type: {tran[2]}, Category: {tran[3]}, Note: {tran[4]}, Date: {tran[5]}')

# ----------------- Show Balance -----------------

def show_balance():
    print(f'Current balance;{db.show_balance()}')

# ----------------- Show by Date or Category -----------------

def show_by_filter():
    choice = int(input("1) Show by date\n2) Show by category\nChoose option: "))
    if choice not in [1, 2]:
        print("Invalid input")
        return
    mode = input("Enter value (yyyy-mm-dd or category): ")
    result = db.show_by(choice, mode)
    if not result:
        print("No matching records found")
    else:
        for tran in result:
            print(f'{tran[0]}) Amount: {tran[1]}, Type: {tran[2]}, Category: {tran[3]}, Note: {tran[4]}, Date: {tran[5]}')

# ----------------- Edit Transaction -----------------

def edit_transaction():
    show_transactions()
    result = db.show_transaction()
    choice = int(input("Which transaction do you want to edit: "))
    if choice < 1 or choice > len(result):
        print("Invalid choice")
        return

    # Default values
    selected = result[choice - 1]

    amount = input("Amount: ")
    amount = float(amount) if amount else float(selected[1])

    type = input("Type: ")
    type = type if type else selected[2]

    category = input("Category: ")
    category = category if category else selected[3]

    note = input("Note: ")
    note = note if note else selected[4]

    date = input("Enter date (yyyy-mm-dd) or leave empty for today: ").strip()
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    updated = [amount, type, category, note, date]
    print(db.edit(updated, choice))

# ----------------- Delete Transaction -----------------

def delete_transaction():
    show_transactions()
    choice = int(input("Which transaction do you want to delete: "))
    db.delete_transaction(choice)

# ----------------- Export to CSV -----------------

def export_csv():
    result = db.show_transaction()
    with open('transactions.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'amount', 'type', 'category', 'note', 'date'])
        for row in result:
            writer.writerow(row)
    print("Exported successfully")
    print("/storage/emulated/0/Documents/Transaction/export.csv")

# ----------------- Generate Report -----------------

def generate_report():
    t1, t2, balance, categories, dates = db.report_transaction()
    print("=== Transaction Report ===")
    print(f"Total income: {t1}")
    print(f"Total expense: {t2}")
    print(f"Balance: {balance}")
    
    print("--- By Category ---")
    for category, amount in categories:
        print(f"{category}: {amount}")
    
    print("--- By Date ---")
    for date, count in dates:
        print(f"{date}: {count}")

# ----------------- Show Chart -----------------

def show_chart():
    db.draw()
    input("Press Enter to continue...")

# ----------------- Main Loop -----------------

while True:
    show_menu()
    try:
        action = int(input("Choose an option: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if action == 1:
        add_transaction()
    elif action == 2:
        show_transactions()
    elif action == 3:
        show_balance()
    elif action == 4:
        show_by_filter()
    elif action == 5:
        edit_transaction()
    elif action == 6:
        delete_transaction()
    elif action == 7:
        export_csv()
    elif action == 8:
        generate_report()
    elif action == 9:
        show_chart()
    elif action == 10:
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")

GUI.add_transaction_form()