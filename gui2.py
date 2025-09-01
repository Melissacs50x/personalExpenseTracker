
import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, CENTER, PRIMARY, SUCCESS, BOTH
from ttkbootstrap.widgets import Treeview
from tkinter import messagebox
from datetime import datetime
import db
from db import delete_transaction
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ===============================
# Table نمایش لیست تراکنش‌ها
# ===============================
def table(window):
    title = ttk.Label(window, text='List of Transactions')
    title.pack(pady=10)

    columns = ['Id', 'Date', 'Amount', 'Type', 'Category', 'Note']
    tree = Treeview(window, columns=columns, show='headings', bootstyle=INFO)

    # تنظیم ستون‌ها
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=CENTER, width=50)

    # گرفتن تراکنش‌ها از دیتابیس
    tn = db.show_transaction()
    tree.tag_configure('even')

    for t in tn:
        tree.insert('', 'end', values=t)

    tree.pack(fill=BOTH, expand=True, pady=10, padx=10)

# ===============================
# فرم افزودن تراکنش جدید
# ===============================
def open_add_transaction_form():
    def save_transaction():
        try:
            amount = float(amount_entry.get())
            type_value = type_var.get()
            category = category_entry.get()
            note = note_entry.get()
            date = date_entry.get().strip() or datetime.now().strftime('%Y-%m-%d')

            db.save_transaction(amount, type_value, category, note, date)
            messagebox.showinfo("Success", "Transaction saved successfully.")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    form = ttk.Toplevel()
    form.title("Add Transaction")
    form.geometry("700x400")
    form.resizable(False, False)

    # Amount
    ttk.Label(form, text="Amount:", font=("Helvetica", 11)).pack(pady=5)
    amount_entry = ttk.Entry(form, width=30)
    amount_entry.pack()

    # Type (Dropdown)
    ttk.Label(form, text="Type:", font=("Helvetica", 11)).pack(pady=5)
    type_var = ttk.StringVar(value="income")
    ttk.Combobox(form, textvariable=type_var, values=["income", "expense"], width=28, state="readonly").pack()

    # Category
    ttk.Label(form, text="Category:", font=("Helvetica", 11)).pack(pady=5)
    category_entry = ttk.Entry(form, width=30)
    category_entry.pack()

    # Note
    ttk.Label(form, text="Note:", font=("Helvetica", 11)).pack(pady=5)
    note_entry = ttk.Entry(form, width=30)
    note_entry.pack()

    # Date
    ttk.Label(form, text="Date (yyyy-mm-dd):", font=("Helvetica", 11)).pack(pady=5)
    date_entry = ttk.Entry(form, width=30)
    date_entry.pack()

    # Save Button
    ttk.Button(form, text="Save", command=save_transaction, bootstyle="primary_outline").pack(pady=15)

# ===============================
# فرم نمایش تمام تراکنش‌ها
# ===============================
def show_form():
    window = ttk.Toplevel()
    window.title('All Transactions')
    window.geometry('960x400')
    window.resizable(False, False)

    table(window)

    btn = ttk.Button(
        window, text='New Transaction',
        command=open_add_transaction_form,
        width=30, bootstyle="primary_outline"
    )
    btn.pack(pady=10)

    window.mainloop()

# ===============================
# فرم نمایش موجودی
# ===============================
def balance_form():
    form = ttk.Toplevel()
    form.title('Transaction Balance')
    form.geometry('400x100')

    bl = db.show_balance()
    lb = ttk.Label(form, text=f'Your Current Balance is: {bl}', font=("Helvetica", 15), justify='left')
    lb.pack(pady=10, padx=10)

    form.resizable(False, False)

# ===============================
# فرم نمایش براساس تاریخ یا دسته‌بندی
# ===============================
def showby_form():
    form = ttk.Toplevel()
    form.title('Show by (Date or Category)')
    form.geometry('500x350')
    form.resizable(False, False)

    ttk.Label(form, text="Show by:", font=("Helvetica", 11)).pack(pady=5)
    combo = ttk.Combobox(form, values=
["Date", "Category"], width=28, state="readonly")
    combo.pack()

    # Frame پویا برای ورودی‌ها
    dy_frame = ttk.Frame(form)
    dy_frame.pack(pady=10, fill='both', expand=True)

    date_label = ttk.Label(dy_frame, text="Date (yyyy-mm-dd):", font=("Helvetica", 11))
    date_entry = ttk.Entry(dy_frame, width=30)
    category_label = ttk.Label(dy_frame, text="Category:", font=("Helvetica", 11))
    category_entry = ttk.Entry(dy_frame, width=30)

    show_btn = ttk.Button(form, text="Show", bootstyle="primary_outline")

    # تابع نمایش نتایج
    def sshow(n, mode):
        columns = ['Id', 'Date', 'Amount', 'Type', 'Category', 'Note']
        tree = Treeview(form, columns=columns, show='headings', bootstyle=INFO)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER, width=50)

        # پاک کردن داده‌های قبلی
        for i in tree.get_children():
            tree.delete(i)

        result = db.show_by(n, mode)
        if not result:
            messagebox.showinfo('Success', 'No match!')
        else:
            title = ttk.Label(form, text='List of Transactions')
            title.pack(pady=10)

            tree.tag_configure('even')
            tree.pack(fill=BOTH, expand=True, pady=10, padx=10)

            for t in result:
                tree.insert('', 'end', values=t)

            btn = ttk.Button(
                form, text='New Transaction',
                command=open_add_transaction_form,
                width=30, bootstyle="primary_outline"
            )
            btn.pack(pady=10)
            form.mainloop()

    # Event برای انتخاب کمبوباکس
    def on(event):
        choice = combo.get()
        if choice == 'Date':
            date_label.pack()
            date_entry.pack()
            show_btn.config(command=lambda: sshow(1, date_entry.get()))
            show_btn.pack(pady=15)
        else:
            category_label.pack()
            category_entry.pack()
            show_btn.config(command=lambda: sshow(2, category_entry.get()))
            show_btn.pack(pady=15)

    combo.bind('<<ComboboxSelected>>', on)

# ===============================
# فرم ویرایش تراکنش
# ===============================
def edit_form():
    def new_edit():
        win = ttk.Toplevel()
        win.title('Edit Transactions')
        win.geometry('400x350')

        # Amount
        ttk.Label(win, text="Amount:", font=("Helvetica", 11)).pack(pady=5)
        amount_entry = ttk.Entry(win, width=30)
        amount_entry.pack()

        # Type (Dropdown)
        ttk.Label(win, text="Type:", font=("Helvetica", 11)).pack(pady=5)
        type_var = ttk.StringVar(value="income")
        com = ttk.Combobox(win, textvariable=type_var, values=["income", "expense"], width=28, state="readonly")
        com.pack()

        # Category
        ttk.Label(win, text="Category:", font=("Helvetica", 11)).pack(pady=5)
        category_entry = ttk.Entry(win, width=30)
        category_entry.pack()

        # Note
        ttk.Label(win, text="Note:", font=("Helvetica", 11)).pack(pady=5)
        note_entry = ttk.Entry(win, width=30)
        note_entry.pack()

        # Date
        ttk.Label(win, text="Date (yyyy-mm-dd):", font=("Helvetica", 11)).pack(pady=5)
        date_entry = ttk.Entry(win, width=30)
        date_entry.pack()

        # تابع ذخیره ویرایش
        def back_edit():
            trans = [amount_entry.get(), com.get(), category_entry.get(), note_entry.get(), date_entry.get()]
            result = db.edit(trans, index_entry.get())
            if not result:
                messagebox.showinfo('Error', 'Something went wrong')
            else:
                messagebox.showinfo('Success', 'Transaction updated')

        ttk.Button(win, text="Edit", command=back_edit, bootstyle="primary_outline").pack(pady=15)

    form = ttk.Toplevel()
    form.title('All Transactions')
    form.geometry('400x350')
    form.resizable(False, False)

    table(form)

    ttk.Label(form, text="Which one do you want to edit?:", font=("Helvetica", 11)).pack(pady=5)
    index_entry = ttk.Entry(form,
 width=30)
    index_entry.pack()

    ttk.Button(form, text="Confirm", command=new_edit, bootstyle="primary_outline").pack(pady=15)

# ===============================
# فرم حذف تراکنش
# ===============================
def delete_form():
    form = ttk.Toplevel()
    form.title('Delete Transactions')
    form.geometry('400x350')
    form.resizable(False, False)

    table(form)

    ttk.Label(form, text="Which one do you want to delete?:", font=("Helvetica", 11)).pack(pady=5)
    index_entry = ttk.Entry(form, width=30)
    index_entry.pack()

    # ادامه کد حذف تراکنش باید اینجا اضافه شود
# ===============================
# فرم حذف تراکنش
# ===============================
def delete_form():
    form = ttk.Toplevel()
    form.title('Delete Transactions')
    form.geometry('400x350')
    form.resizable(False, False)

    table(form)

    ttk.Label(form, text="Which one do you want to delete?:", font=("Helvetica", 11)).pack(pady=5)
    index_entry = ttk.Entry(form, width=30)
    index_entry.pack()

    btn = ttk.Button(
        form,
        text='Delete',
        command=lambda: messagebox.showinfo(
            'Deleted Successfully' if delete_transaction(index_entry.get()) else 'Something went wrong'
        )
    )
    btn.pack(pady=10)

# ===============================
# فرم خروجی گرفتن از تراکنش‌ها به CSV
# ===============================
def export_form():
    result = db.show_transaction()
    with open('transactions.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'amount', 'type', 'category', 'note', 'date'])
        for row in result:
            writer.writerow(row)

    messagebox.showinfo(
        'SUCCESS',
        "Exported successfully in: /storage/emulated/0/Documents/Transaction/export.csv"
    )

# ===============================
# فرم گزارش تراکنش‌ها
# ===============================
def report_form():
    form = ttk.Toplevel()
    form.title('Generate Report')
    form.geometry('500x350')
    form.resizable(False, False)

    record = db.report_transaction()

    ttk.Label(form, text=f"Total Income: {record[0]}", font=("Helvetica", 11)).pack(pady=5)
    ttk.Label(form, text=f"Total Expense: {record[1]}", font=("Helvetica", 11)).pack(pady=5)
    ttk.Label(form, text=f"Balance: {record[2]}", font=("Helvetica", 11)).pack(pady=5)
    ttk.Label(form, text=f"Total By Category: {record[3]}", font=("Helvetica", 11)).pack(pady=5)
    ttk.Label(form, text=f"Transaction Count By Date: {record[4]}", font=("Helvetica", 11)).pack(pady=5)

# ===============================
# فرم نمایش نمودار درآمد و هزینه
# ===============================
def chart_form():
    form = ttk.Toplevel()
    form.title('Show Chart')
    form.geometry('400x400')

    total_income, total_expense, *_ = db.report_transaction()

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
    colors = ['#ff9999', '#66b3ff']

    print(f"Drawing chart: {values}")
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title('Income vs Expense')
    plt.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=form)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

# ===============================
# برنامه اصلی
# ===============================
if __name__ == "__main__":
    app = ttk.Window(themename="morph")
    app.title("Personal Expense Tracker")
    app.geometry("300x400")

    # دکمه‌های منو
    ttk.Button(app, text="Add Transaction", width=25, command=open_add_transaction_form, bootstyle="primary_outline").pack(pady=5)
    ttk.Button(app, text='Show All Transactions', width=25, command=show_form, bootstyle='primary_outline').pack(pady=5)
    ttk.Button(app, text='Show Balance', width=25, command=balance_form, bootstyle='primary_outline').pack(pady=5)
    ttk.Button(app, text='Show by (Date or Category)', width=25, command=showby_form, bootstyle='primary_outline').pack(pady=5)
    ttk.Button(app, text='Edit Transaction', width=25, command=edit_form, bootstyle='primary_outline').pack(pady=5)
    ttk.Button(app, text='Delete Transaction', width=25, command=delete_form, bootstyle='primary_outline').pack(pady=5)
    ttk.Button(app, text='Export to CSV', width=25, command=export_form, bootstyle='primary_outline').pack(pady=5)
    ttk.Button(app, text='Generate Report', width=25, command=report_form, bootstyle='primary_outline').pack(pady=5)
    ttk.Button(app, text='Draw a Chart', width=25, command=chart_form, bootstyle='primary_outline').pack(pady=5)

    app.mainloop()