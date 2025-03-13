import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class TransactionInput:
    """Component for inputting new transactions"""
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        
        # Create frame for transaction input
        self.frame = ttk.Frame(parent, style="Card.TFrame")
        self.frame.pack(fill="x", pady=(0, 20))
        
        # Add title
        title_label = ttk.Label(
            self.frame, 
            text="Add New Transaction",
            font=("Inter", 16, "bold"),
            style="CardTitle.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 20))
        
        # Configure grid columns
        self.frame.columnconfigure(0, weight=1)  # Description
        self.frame.columnconfigure(1, weight=1)  # Amount
        self.frame.columnconfigure(2, weight=1)  # Type
        self.frame.columnconfigure(3, weight=1)  # Button
        
        # Description input
        desc_label = ttk.Label(self.frame, text="Description:", style="InputLabel.TLabel")
        desc_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 5))
        
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(
            self.frame, 
            textvariable=self.description_var,
            style="Input.TEntry",
            width=25
        )
        self.description_entry.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        # Amount input
        amount_label = ttk.Label(self.frame, text="Amount ($):", style="InputLabel.TLabel")
        amount_label.grid(row=1, column=1, sticky="w", padx=15, pady=(0, 5))
        
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(
            self.frame, 
            textvariable=self.amount_var,
            style="Input.TEntry",
            width=15
        )
        self.amount_entry.grid(row=2, column=1, sticky="ew", padx=15, pady=(0, 15))
        
        # Transaction type
        type_label = ttk.Label(self.frame, text="Type:", style="InputLabel.TLabel")
        type_label.grid(row=1, column=2, sticky="w", padx=15, pady=(0, 5))
        
        self.type_var = tk.StringVar(value="Income")
        self.type_combo = ttk.Combobox(
            self.frame, 
            textvariable=self.type_var,
            values=["Income", "Expense"],
            state="readonly",
            style="Input.TCombobox",
            width=15
        )
        self.type_combo.grid(row=2, column=2, sticky="ew", padx=15, pady=(0, 15))
        
        # Add button
        self.add_button = ttk.Button(
            self.frame, 
            text="Add Transaction",
            style="Primary.TButton",
            command=self.add_transaction
        )
        self.add_button.grid(row=2, column=3, sticky="ew", padx=15, pady=(0, 15))
    
    def add_transaction(self):
        """Add a new transaction"""
        # Get input values
        description = self.description_var.get().strip()
        amount_str = self.amount_var.get().strip()
        transaction_type = self.type_var.get()
        
        # Validate inputs
        if not description:
            messagebox.showerror("Input Error", "Please enter a description.")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Input Error", "Amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return
        
        # Create transaction object
        transaction = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "description": description,
            "amount": amount,
            "type": transaction_type
        }
        
        # Call the callback function
        self.callback(transaction)
        
        # Clear inputs
        self.description_var.set("")
        self.amount_var.set("")
        self.type_var.set("Income")
        
        # Set focus back to description
        self.description_entry.focus()


class TransactionList:
    """Component for displaying transaction history"""
    
    def __init__(self, parent):
        self.parent = parent
        self.transactions = []
        
        # Create frame for transaction list
        self.frame = ttk.Frame(parent, style="Card.TFrame")
        self.frame.pack(fill="both", expand=True)
        
        # Add title
        title_label = ttk.Label(
            self.frame, 
            text="Transaction History",
            font=("Inter", 16, "bold"),
            style="CardTitle.TLabel"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 20))
        
        # Create search frame
        search_frame = ttk.Frame(self.frame, style="Card.TFrame")
        search_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Add search label
        search_label = ttk.Label(search_frame, text="Search:", style="InputLabel.TLabel")
        search_label.pack(side="left", padx=(0, 10))
        
        # Add search entry
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_transactions)
        search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var,
            style="Input.TEntry",
            width=30
        )
        search_entry.pack(side="left", fill="x", expand=True)
        
        # Create container for treeview and scrollbar
        tree_container = ttk.Frame(self.frame, style="Card.TFrame")
        tree_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Create custom style for the treeview
        style = ttk.Style()
        style.configure(
            "TransactionTree.Treeview",
            background="#1F2937",
            foreground="#F9FAFB",
            fieldbackground="#1F2937",
            font=("Inter", 10),
            rowheight=40,
            borderwidth=0
        )
        
        style.configure(
            "TransactionTree.Treeview.Heading",
            background="#3730A3",
            foreground="#FFFFFF",
            font=("Inter", 11, "bold"),
            relief="raised",
            borderwidth=1,
            padding=10
        )
        
        style.map(
            "TransactionTree.Treeview.Heading",
            background=[('active', '#4F46E5')],
            foreground=[('active', '#FFFFFF')]
        )
        
        style.map(
            "TransactionTree.Treeview",
            background=[('selected', '#4F46E5')],
            foreground=[('selected', '#F9FAFB')]
        )
        
        # Create treeview for transactions
        self.tree = ttk.Treeview(
            tree_container,
            columns=("date", "description", "type", "amount"),
            show="headings",
            style="TransactionTree.Treeview",
            height=10
        )
        
        # Configure columns
        self.tree.heading("date", text="Date")
        self.tree.heading("description", text="Description")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Amount")
        
        self.tree.column("date", width=100, anchor="w")
        self.tree.column("description", width=250, anchor="w")
        self.tree.column("type", width=100, anchor="center")
        self.tree.column("amount", width=100, anchor="e")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Show placeholder message if no transactions
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder message if no transactions"""
        if not self.transactions:
            # Clear any existing placeholder
            for item in self.tree.get_children():
                if item.startswith("placeholder"):
                    self.tree.delete(item)
            
            # Add placeholder message
            self.tree.insert("", "end", iid="placeholder", values=("", "No transactions yet. Add a new transaction to get started.", "", ""))
    
    def add_transaction(self, transaction, update_ui=True):
        """Add a transaction to the list"""
        # Add to internal list
        self.transactions.append(transaction)
        
        # Clear placeholder if it exists
        for item in self.tree.get_children():
            if item.startswith("placeholder"):
                self.tree.delete(item)
        
        # Format amount with currency symbol
        formatted_amount = f"${transaction['amount']:.2f}"
        
        # Add to treeview
        item_id = self.tree.insert(
            "",
            "end",
            values=(
                transaction["date"],
                transaction["description"],
                transaction["type"],
                formatted_amount
            )
        )
        
        # Apply tag based on transaction type
        if transaction["type"] == "Income":
            self.tree.tag_configure("income", foreground="#10B981")
            self.tree.item(item_id, tags=("income",))
        else:
            self.tree.tag_configure("expense", foreground="#EF4444")
            self.tree.item(item_id, tags=("expense",))
        
        # Scroll to the new item
        if update_ui:
            self.tree.see(item_id)
            
            # Update search filter
            self.filter_transactions()
    
    def filter_transactions(self, *args):
        """Filter transactions based on search query"""
        search_term = self.search_var.get().lower()
        
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # If no transactions, show placeholder
        if not self.transactions:
            self.show_placeholder()
            return
        
        # Filter and add matching transactions
        has_matches = False
        for transaction in self.transactions:
            # Check if transaction matches search term
            if (search_term in transaction["description"].lower() or
                search_term in transaction["date"].lower() or
                search_term in transaction["type"].lower() or
                search_term in str(transaction["amount"])):
                
                # Format amount with currency symbol
                formatted_amount = f"${transaction['amount']:.2f}"
                
                # Add to treeview
                item_id = self.tree.insert(
                    "",
                    "end",
                    values=(
                        transaction["date"],
                        transaction["description"],
                        transaction["type"],
                        formatted_amount
                    )
                )
                
                # Apply tag based on transaction type
                if transaction["type"] == "Income":
                    self.tree.tag_configure("income", foreground="#10B981")
                    self.tree.item(item_id, tags=("income",))
                else:
                    self.tree.tag_configure("expense", foreground="#EF4444")
                    self.tree.item(item_id, tags=("expense",))
                
                has_matches = True
        
        # Show no matches message if needed
        if not has_matches:
            self.tree.insert("", "end", iid="no_matches", values=("", f"No transactions matching '{search_term}'", "", ""))
    
    def clear_transactions(self):
        """Clear all transactions"""
        # Clear internal list
        self.transactions = []
        
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Show placeholder
        self.show_placeholder()
    
    def get_all_transactions(self):
        """Get all transactions"""
        return self.transactions