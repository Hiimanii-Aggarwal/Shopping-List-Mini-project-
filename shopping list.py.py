import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Frame, StringVar, OptionMenu
import json
import os

class ShoppingListApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do Shopping List")
        master.configure(bg="#f0f0f0")  # Light gray background

        # Create a frame for the Listbox and Scrollbar
        frame = Frame(master)
        frame.pack(pady=10)

        # Listbox to display items
        self.listbox = Listbox(frame, width=50, height=15, selectmode=tk.SINGLE, bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar for the Listbox
        self.scrollbar = Scrollbar(frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to the listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Entry box to add new items
        self.item_entry = tk.Entry(master, width=50, font=("Arial", 12))
        self.item_entry.pack(pady=10)

        # Dropdown menu for categories
        self.categories = ["Grocery", "Electronics", "Clothing", "Miscellaneous"]
        self.selected_category = StringVar(master)
        self.selected_category.set(self.categories[0])  # Default value
        self.category_menu = OptionMenu(master, self.selected_category, *self.categories)
        self.category_menu.pack(pady=5)

        # Add button to add items
        self.add_button = tk.Button(master, text="Add Item", command=self.add_item, bg="#4CAF50", fg="#ffffff", font=("Arial", 12))
        self.add_button.pack(pady=5)

        # Edit button to edit selected items
        self.edit_button = tk.Button(master, text="Edit Selected Item", command=self.edit_item, bg="#2196F3", fg="#ffffff", font=("Arial", 12))
        self.edit_button.pack(pady=5)

        # Remove button to remove selected items
        self.remove_button = tk.Button(master, text="Remove Selected Item", command=self.remove_item, bg="#F44336", fg="#ffffff", font=("Arial", 12))
        self.remove_button.pack(pady=5)

        # Clear button to clear the list
        self.clear_button = tk.Button(master, text="Clear List", command=self.clear_list, bg="#FF9800", fg="#ffffff", font=("Arial", 12))
        self.clear_button.pack(pady=5)

        # Sort button to sort items
        self.sort_button = tk.Button(master, text="Sort Items", command=self.sort_items, bg="#9C27B0", fg="#ffffff", font=("Arial", 12))
        self.sort_button.pack(pady=5)

        # Select All button
        self.select_all_button = tk.Button(master, text="Select All", command=self.select_all_items, bg="#FF5722", fg="#ffffff", font=("Arial", 12))
        self.select_all_button.pack(pady=5)

        # Load the shopping list from a file
        self.load_items()

    def add_item(self):
        item = self.item_entry.get()
        category = self.selected_category.get()
        if item:
            selected_item_index = self.listbox.curselection()
            if selected_item_index:  # If editing an existing item
                self.listbox.delete(selected_item_index[0])  # Remove the old item
            self.listbox.insert(tk.END, f"{item} [{category}]")  # Add new/edited item
            self.item_entry.delete(0, tk.END)  # Clear the entry box
            self.save_items()
        else:
            messagebox.showwarning("Warning", "You must enter an item.")

    def edit_item(self):
        try:
            selected_item_index = self.listbox.curselection()[0]
            current_item = self.listbox.get(selected_item_index)
            item_name = current_item.split(' [')[0]  # Get item name without category
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(0, item_name)  # Pre-fill the entry box for editing
            self.listbox.selection_clear(0, tk.END)  # Clear selection to avoid confusion
        except IndexError:
            messagebox.showwarning("Warning", "You must select an item to edit.")

    def remove_item(self):
        try:
            selected_item_index = self.listbox.curselection()[0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
                self.listbox.delete(selected_item_index)
                self.save_items()
        except IndexError:
            messagebox.showwarning("Warning", "You must select an item to remove.")

    def clear_list(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the entire list?"):
            self.listbox.delete(0, tk.END)  # Clear the entire list
            self.save_items()

    def sort_items(self):
        items = list(self.listbox.get(0, tk.END))
        items.sort()  # Sort the list of items
        self.listbox.delete(0, tk.END)  # Clear the Listbox
        for item in items:
            self.listbox.insert(tk.END, item)  # Insert sorted items back to Listbox
        self.save_items()

    def select_all_items(self):
        self.listbox.select_set(0, tk.END)  # Select all items in the Listbox

    def save_items(self):
        items = list(self.listbox.get(0, tk.END))
        with open("shopping_list.json", "w") as f:
            json.dump(items, f)

    def load_items(self):
        if os.path.exists("shopping_list.json"):
            with open("shopping_list.json", "r") as f:
                items = json.load(f)
                for item in items:
                    self.listbox.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingListApp(root)
    root.mainloop()
