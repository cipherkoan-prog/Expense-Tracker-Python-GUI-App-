import json
from datetime import datetime
import matplotlib.pyplot as plt
from openpyxl import Workbook
import tkinter as tk
from tkinter import messagebox 
import os

FILE_NAME="data.json"

# Load expenses from file
def load_expenses():
    try:
        with open(FILE_NAME,"r") as file:
            return json.load(file)
    except:
        return []
    
# Save expenses to file
def save_expenses(expenses):
    with open(FILE_NAME,"w") as file:
        json.dump(expenses,file,indent=4)

expenses=load_expenses()

# Gui Function
def add_expense():
    try:
        amount=float(amount_entry.get())
        category=category_entry.get()
        date=datetime.now().strftime("%Y-%m-%d")

        expense={
            "amount": amount,
            "category": category,
            "date": date
        }

        expenses.append(expense)
        save_expenses(expenses)

        messagebox.showinfo("Success", "Expense added!")

        # Clear input fields
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)

        view_expenses() # auto update list

    except:
        messagebox.showerror("Error", "Invalid input!")

def view_expenses():
    expense_listbox.delete(0, tk.END) # clear old data
    
    for i, exp in enumerate(expenses, start=1):
        text=f"{i}. {exp['category']} - ₹{exp['amount']} on {exp['date']}"
        expense_listbox.insert(tk.END, text)

def delete_selected():
    try:
        selected_index=expense_listbox.curselection()[0]

        remove=expenses.pop(selected_index)
        save_expenses(expenses)

        messagebox.showinfo("Deleted", f"{remove['category']} ₹{remove['amount']} deleted!")

        view_expenses()
    except:
        messagebox.showerror("Error", "Please select an item to delete")

def show_chart():
    if not expenses:
        messagebox.showerror("Error", "No expenses to show")
        return

    
    category_totals={}

    # Calculate totals per category
    for exp in expenses:
        category=exp["category"]
        amount=exp["amount"]

        if category in category_totals:
            category_totals[category]+=amount
        else:
            category_totals[category]=amount

    # prepare data for chart
    categories=list(category_totals.keys())
    amounts=list(category_totals.values())

    # Plot chart
    plt.figure()
    plt.bar(categories, amounts)
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.title("Expense Distribution by Category")
    plt.show()

def show_total():
    if not expenses:
        messagebox.showinfo("Total", "No expenses yet.")
        return

    total=sum(exp["amount"] for exp in expenses)
    
    messagebox.showinfo("Total Expenses", f"Total ₹{total}")
                        
def filter_expenses():
    category=filter_entry.get().lower()

    expense_listbox.delete(0, tk.END)

    found=False

    for i, exp in enumerate(expenses, start=1):
        if exp["category"].lower()==category:
            text=f"{i}. {exp['category']} - ₹{exp['amount']} on {exp['date']}"
            expense_listbox.insert(tk.END, text)
            found=True

    if not found:
        messagebox.showinfo("Result", "No matching expenses found")

def monthly_report_gui():
    month=month_entry.get().strip()

    expense_listbox.delete(0, tk.END)

    total=0
    found=False

    for i, exp in enumerate(expenses, start=1):
        if exp["date"].startswith(month):
            text = f"{i}. {exp['category']} - ₹{exp['amount']} on {exp['date']}"
            expense_listbox.insert(tk.END, text)
            total += exp["amount"]
            found = True

    if not found:
       messagebox.showinfo("Report", "No expenses found for this month.")
    else:
        messagebox.showinfo("Monthly Total", f"Total for {month}: ₹{total}")

def export_to_excel():
    if not expenses:
        messagebox.showerror("Error", "No expenses to export.")
        return
    
    wb=Workbook()
    ws=wb.active
    ws.title="Expenses"

    # Header row
    ws.append(["Amount","Category","Date"])

    # Add data
    for exp in expenses:
        ws.append([exp["amount"], exp["category"], exp["date"]])

    ws.append([])
    ws.append(["", "Total", sum(exp["amount"] for exp in expenses)])

    # Save file
    wb.save("expenses.xlsx")

    os.startfile("expenses.xlsx")

    messagebox.showinfo("Success", "Exported to expenses.xlsx!")


# GUI
root= tk.Tk()
root.title("Expense Tracker")
root.geometry("400x700")

# Labels
tk.Label(root,text="Amount").pack()
amount_entry=tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Category").pack()
category_entry=tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Filter Category").pack()
filter_entry = tk.Entry(root)
filter_entry.pack()

tk.Label(root, text="Enter Month (YYYY-MM)").pack()
month_entry = tk.Entry(root)
month_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="View Expenses", command=view_expenses).pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_selected).pack(pady=5)
tk.Button(root, text="Show Chart", command=show_chart).pack(pady=5)
tk.Button(root, text="Show Total", command=show_total).pack(pady=5)
tk.Button(root, text="Filter", command=filter_expenses).pack(pady=5)
tk.Button(root, text="Show All", command=view_expenses).pack(pady=5)
tk.Button(root, text="Monthly Report", command=monthly_report_gui).pack(pady=5)
tk.Button(root, text="Export to Excel", command=export_to_excel).pack(pady=5)

tk.Label(root, text="Expenses").pack()
expense_listbox=tk.Listbox(root, width=50)
expense_listbox.config(selectbackground="red")
expense_listbox.pack()



root.mainloop()

