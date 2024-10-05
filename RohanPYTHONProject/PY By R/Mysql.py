import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# Database connection parameters
db_config = {
    'user': 'root',
    'password': 'Rohan15@',
    'host': 'localhost',
    'database': 'rohanpy',
}


# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(**db_config)


# Function to insert data into the database
def insert_data():
    name = entry_name.get()
    age = entry_age.get()

    if name and age:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
            conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            cursor.close()
            conn.close()
            clear_entries()
            view_data()  # Refresh the data
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
    else:
        messagebox.showwarning("Input Error", "Please enter both name and age.")


# Function to view data from the database
def view_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        records = cursor.fetchall()

        # Clear the treeview
        for item in tree.get_children():
            tree.delete(item)

        for row in records:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")


# Function to delete data from the database
def delete_data():
    selected_item = tree.selection()
    if selected_item:
        name = tree.item(selected_item, 'values')[1]
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE name = %s", (name,))
            conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully!")
            cursor.close()
            conn.close()
            view_data()  # Refresh the data
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
    else:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")


# Function to clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)


# Create main window
root = tk.Tk()
root.title("MySQL GUI Application")

# Create and place labels and entry fields
label_name = tk.Label(root, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=10)

entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)

label_age = tk.Label(root, text="Age:")
label_age.grid(row=1, column=0, padx=10, pady=10)

entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, padx=10, pady=10)

# Create buttons
button_insert = tk.Button(root, text="Insert", command=insert_data)
button_insert.grid(row=2, column=0, padx=10, pady=10)

button_view = tk.Button(root, text="View", command=view_data)
button_view.grid(row=2, column=1, padx=10, pady=10)

button_delete = tk.Button(root, text="Delete", command=delete_data)
button_delete.grid(row=2, column=2, padx=10, pady=10)

# Create Treeview for displaying records
columns = ("ID", "Name", "Age")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Run the application
view_data()  # Load initial data
root.mainloop()
