import sqlite3
import matplotlib.pyplot as plt
import os

# ===============================
# پایگاه داده: ایجاد جدول
# ===============================
def init_db():
    """
    Initialize the database and create the transactions table if it doesn't exist.
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            type TEXT,
            category TEXT,
            note TEXT,
            date TEXT
        )
    ''')
    con.commit()
    con.close()

# ===============================
# افزودن تراکنش
# ===============================
def save_transaction(amount, type, category, note, date):
    """
    Save a new transaction to the database.
    """
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('''
        INSERT INTO transactions(amount, type, category, note, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (amount, type, category, note, date))
    con.commit()
    con.close()
    print('Saved successfully')

# ===============================
# مشاهده همه تراکنش‌ها
# ===============================
def show_transaction():
    """
    Retrieve and return all transactions.
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM transactions')
    result = cur.fetchall()
    con.close()
    return result

# ===============================
# مشاهده موجودی فعلی
# ===============================
def show_balance():
    """
    Calculate and return the current balance.
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT type, amount FROM transactions')
    rows = cur.fetchall()

    balance = 0
    for type, amount in rows:
        if type.lower() == 'income':
            balance += amount
        elif type.lower() == 'expense':
            balance -= amount

    con.close()
    return balance

# ===============================
# فیلتر بر اساس تاریخ یا دسته‌بندی
# ===============================
def show_by(n, mode):
    """
    Filter transactions:
    - n=1: filter by date
    - n=2: filter by category
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    if n == 1:
        cur.execute('SELECT * FROM transactions WHERE date = ?', (mode,))
    elif n == 2:
        cur.execute('SELECT * FROM transactions WHERE category = ?', (mode,))

    rows = cur.fetchall()
    con.close()
    return rows

# ===============================
# ویرایش تراکنش
# ===============================
def edit(trans, n):
    """
    Edit a transaction by ID.
    trans: [amount, type, category, note, date]
    n: transaction ID
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('''
        UPDATE transactions
        SET amount = ?, type = ?, category = ?, note = ?, date = ?
        WHERE id = ?
    ''', (trans[0], trans[1], trans[2], trans[3], trans[4], n))
    con.commit()
    con.close()
    return 'updated successfully'

# ===============================
# حذف تراکنش
# ===============================
def delete_transaction(n):
    """
    Delete a transaction by ID.
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('DELETE FROM transactions WHERE id = ?', (n,))
    con.commit()
    con.close()
    print('Deleted successfully')

# ===============================
# گزارش مالی
# ===============================
def report_transaction():
    """
    Generate a financial report:
    - Total income
    - Total expense
    - Balance
    - Total by category
    - Transaction count by date
    """
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    # محاسبه درآمد و هزینه کل
    cur.execute('SELECT type, amount FROM transactions')
    rows = cur.fetchall()

    total_income = 0
    total_expense = 0
    for type, amount in rows:
        if type.lower() == 'income':
            total_income += amount
        elif type.lower() == 'expense':
            total_expense += amount

    balance = total_income - total_expense

    # مجموع بر اساس دسته‌بندی
    cur.execute('SELECT category, SUM(amount) FROM transactions GROUP BY category')
    result1 = cur.fetchall()

    # تعداد تراکنش‌ها بر اساس تاریخ
    cur.execute('SELECT date, COUNT(*) FROM transactions GROUP BY date')
    result2 = cur.fetchall()

    con.close()
    return total_income, total_expense, balance, result1, result2

# ===============================
# رسم نمودار دایره‌ای درآمد و هزینه
# ===============================
def draw():
    """
    Draw a pie chart of income vs expense and save it to device storage.
    """
    total_income, total_expense, *_ = report_transaction()

    try:
        income = float(total_income)
        expense = float(total_expense)
    except:
        print("Error: Invalid values for chart.")
        return

    if income == 0 and expense == 0:
        print("No data to display in chart.")
        return

    labels = ['Income', 'Expense']
    values = [income, expense]

    print(f"Drawing chart: {values}")

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Income vs Expense')
    plt.axis('equal')

    # مسیر ذخیره‌سازی نمودار
    path = '/storage/emulated/0/Documents/Transaction'
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, 'chart.png')
    plt.savefig(file_path)
    print(f"Chart saved at: {file_path}")
    plt.show()