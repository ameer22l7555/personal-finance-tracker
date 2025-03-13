import tkinter as tk
from tkinter import ttk, messagebox
from src.components.loading_screen import LoadingScreen
from src.components.transactions import TransactionInput, TransactionList
from src.components.charts import FinancialCharts
from src.styles.theme import AppTheme
from src.utils.animations import ValueAnimator
from src.utils.file_handler import FileHandler
import time
import datetime

class PersonalFinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        
        # Initialize theme
        self.theme = AppTheme()
        self.style = ttk.Style()
        self.theme.setup_styles(self.style)
        
        # Configure root window
        self.root.configure(bg=self.theme.colors['background'])
        
        # Apply global fixes for treeview headers
        self.fix_treeview_headers()
        
        # Show loading screen
        loading = LoadingScreen(root)
        
        # Set minimum window size
        self.root.minsize(1200, 800)
        
        # Make window fullscreen by default
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Initialize transaction data
        self.transactions = []
        self.total_income = 0.0
        self.total_expenses = 0.0
        
        # Setup menu
        self.setup_menu()
        
        # Create main container with modern styling
        self.main_container = ttk.Frame(self.root, padding="20", style="Main.TFrame")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(2, weight=1)
        self.main_container.grid_columnconfigure(0, weight=3)
        self.main_container.grid_columnconfigure(1, weight=2)
        
        # Setup UI components
        self.setup_header()
        self.setup_balance_section()
        self.setup_main_content()
        
        # Apply theme overrides for native widgets
        self.apply_native_widget_styles()
    
    def setup_menu(self):
        """Setup application menu with file operations"""
        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Create File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Add menu items
        file_menu.add_command(label="New", command=self.new_data)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Load", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_command(label="Import from CSV", command=self.import_from_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Create Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        
        # Add help menu items
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
    
    def new_data(self):
        """Clear all data and start fresh"""
        if messagebox.askyesno("New Data", "Are you sure you want to clear all data? This cannot be undone."):
            # Reset transaction data
            self.transactions = []
            self.total_income = 0.0
            self.total_expenses = 0.0
            
            # Update UI
            self.income_label.config(text="$0.00")
            self.expense_label.config(text="$0.00")
            self.balance_label.config(text="$0.00")
            
            # Clear transaction list
            self.transaction_list.clear_transactions()
            
            # Update charts
            self.charts.update_charts([])
            
            messagebox.showinfo("New Data", "All data has been cleared.")
    
    def save_data(self):
        """Save financial data to a file"""
        # Prepare data to save
        data = {
            "transactions": self.transaction_list.get_all_transactions(),
            "total_income": self.total_income,
            "total_expenses": self.total_expenses,
            "saved_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save data using FileHandler
        if FileHandler.save_data(data):
            messagebox.showinfo("Save Successful", "Your financial data has been saved successfully.")
    
    def load_data(self):
        """Load financial data from a file"""
        # Confirm if there's unsaved data
        if self.transactions and messagebox.askyesno("Unsaved Data", 
                                                   "Loading will replace your current data. Continue?"):
            # Load data using FileHandler
            data = FileHandler.load_data()
            
            if data:
                # Update transaction data
                self.transactions = data.get("transactions", [])
                self.total_income = data.get("total_income", 0.0)
                self.total_expenses = data.get("total_expenses", 0.0)
                
                # Update UI
                self.income_label.config(text=f"${self.total_income:.2f}")
                self.expense_label.config(text=f"${self.total_expenses:.2f}")
                self.balance_label.config(text=f"${self.total_income - self.total_expenses:.2f}")
                
                # Update transaction list
                self.transaction_list.clear_transactions()
                for transaction in self.transactions:
                    self.transaction_list.add_transaction(transaction, update_ui=False)
                
                # Update charts
                self.charts.update_charts(self.transactions)
                
                # Show success message with saved date if available
                saved_date = data.get("saved_date", "Unknown")
                messagebox.showinfo("Load Successful", 
                                   f"Your financial data has been loaded successfully.\nLast saved: {saved_date}")
        elif not self.transactions:
            # If no current data, load without confirmation
            data = FileHandler.load_data()
            
            if data:
                # Update transaction data
                self.transactions = data.get("transactions", [])
                self.total_income = data.get("total_income", 0.0)
                self.total_expenses = data.get("total_expenses", 0.0)
                
                # Update UI
                self.income_label.config(text=f"${self.total_income:.2f}")
                self.expense_label.config(text=f"${self.total_expenses:.2f}")
                self.balance_label.config(text=f"${self.total_income - self.total_expenses:.2f}")
                
                # Update transaction list
                self.transaction_list.clear_transactions()
                for transaction in self.transactions:
                    self.transaction_list.add_transaction(transaction, update_ui=False)
                
                # Update charts
                self.charts.update_charts(self.transactions)
                
                # Show success message with saved date if available
                saved_date = data.get("saved_date", "Unknown")
                messagebox.showinfo("Load Successful", 
                                   f"Your financial data has been loaded successfully.\nLast saved: {saved_date}")
    
    def export_to_csv(self):
        """Export transaction data to CSV"""
        if not self.transactions:
            messagebox.showinfo("No Data", "There is no data to export.")
            return
        
        if FileHandler.export_to_csv(self.transactions):
            messagebox.showinfo("Export Successful", "Your financial data has been exported to CSV successfully.")
    
    def import_from_csv(self):
        """Import transaction data from CSV"""
        # Confirm if there's unsaved data
        if self.transactions and messagebox.askyesno("Unsaved Data", 
                                                   "Importing will replace your current data. Continue?"):
            transactions = FileHandler.import_from_csv()
            
            if transactions:
                # Reset current data
                self.transactions = []
                self.total_income = 0.0
                self.total_expenses = 0.0
                
                # Process imported transactions
                for transaction in transactions:
                    if transaction['type'] == "Income":
                        self.total_income += transaction['amount']
                    else:
                        self.total_expenses += transaction['amount']
                
                # Update UI
                self.income_label.config(text=f"${self.total_income:.2f}")
                self.expense_label.config(text=f"${self.total_expenses:.2f}")
                self.balance_label.config(text=f"${self.total_income - self.total_expenses:.2f}")
                
                # Update transaction list
                self.transaction_list.clear_transactions()
                for transaction in transactions:
                    self.transaction_list.add_transaction(transaction, update_ui=False)
                
                # Update charts
                self.charts.update_charts(transactions)
                
                # Update transactions list
                self.transactions = transactions
                
                messagebox.showinfo("Import Successful", 
                                   f"Successfully imported {len(transactions)} transactions.")
        elif not self.transactions:
            # If no current data, import without confirmation
            transactions = FileHandler.import_from_csv()
            
            if transactions:
                # Process imported transactions
                for transaction in transactions:
                    if transaction['type'] == "Income":
                        self.total_income += transaction['amount']
                    else:
                        self.total_expenses += transaction['amount']
                
                # Update UI
                self.income_label.config(text=f"${self.total_income:.2f}")
                self.expense_label.config(text=f"${self.total_expenses:.2f}")
                self.balance_label.config(text=f"${self.total_income - self.total_expenses:.2f}")
                
                # Update transaction list
                self.transaction_list.clear_transactions()
                for transaction in transactions:
                    self.transaction_list.add_transaction(transaction, update_ui=False)
                
                # Update charts
                self.charts.update_charts(transactions)
                
                # Update transactions list
                self.transactions = transactions
                
                messagebox.showinfo("Import Successful", 
                                   f"Successfully imported {len(transactions)} transactions.")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About Personal Finance Tracker", 
                           "Personal Finance Tracker v1.0\n\n"
                           "A modern application for tracking personal finances.\n\n"
                           "© 2025 Finance Tracker Team")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
        Personal Finance Tracker Help
        
        File Menu:
        - New: Clear all data and start fresh
        - Save: Save your financial data to a file
        - Load: Load previously saved financial data
        - Export to CSV: Export your transactions to a CSV file
        - Import from CSV: Import transactions from a CSV file
        - Exit: Close the application
        
        Adding Transactions:
        1. Enter a description
        2. Enter the amount
        3. Select the transaction type (Income/Expense)
        4. Click "Add Transaction"
        
        Viewing Data:
        - The top section shows your total income, expenses, and net balance
        - The left panel shows your transaction history
        - The right panel displays charts visualizing your financial data
        """
        messagebox.showinfo("Help", help_text)
    
    def fix_treeview_headers(self):
        """Apply global fixes for treeview headers"""
        # Fix for Treeview headers not showing in some environments
        style = self.style
        
        # Configure all Treeview headers to be visible
        style.configure(
            "Treeview.Heading",
            background="#3730A3",
            foreground="#FFFFFF",
            font=("Inter", 11, "bold"),
            relief="raised",
            borderwidth=1,
            padding=10
        )
        
        # Configure hover effect
        style.map(
            "Treeview.Heading",
            background=[('active', '#4F46E5')],
            foreground=[('active', '#FFFFFF')]
        )
        
        # Configure the Treeview itself
        style.configure(
            "Treeview",
            background="#1F2937",
            foreground="#F9FAFB",
            fieldbackground="#1F2937",
            font=("Inter", 10),
            rowheight=40,
            borderwidth=0
        )
        
        # Configure selection colors
        style.map(
            "Treeview",
            background=[('selected', '#4F46E5')],
            foreground=[('selected', '#F9FAFB')]
        )
    
    def apply_native_widget_styles(self):
        """Apply theme to native widgets that don't respect ttk styling"""
        # Configure Treeview colors globally
        self.root.option_add('*TCombobox*Listbox.background', self.theme.colors['input_bg'])
        self.root.option_add('*TCombobox*Listbox.foreground', self.theme.colors['text'])
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.theme.colors['primary'])
        self.root.option_add('*TCombobox*Listbox.selectForeground', self.theme.colors['text'])
        
        # Configure Entry widget colors
        self.root.option_add('*Entry.background', self.theme.colors['input_bg'])
        self.root.option_add('*Entry.foreground', self.theme.colors['text'])
        self.root.option_add('*Entry.insertBackground', self.theme.colors['text'])
        
        # Configure Listbox colors
        self.root.option_add('*Listbox.background', self.theme.colors['input_bg'])
        self.root.option_add('*Listbox.foreground', self.theme.colors['text'])
        self.root.option_add('*Listbox.selectBackground', self.theme.colors['primary'])
        self.root.option_add('*Listbox.selectForeground', self.theme.colors['text'])
        
        # Configure Menu colors
        self.root.option_add('*Menu.background', self.theme.colors['card_bg'])
        self.root.option_add('*Menu.foreground', self.theme.colors['text'])
        self.root.option_add('*Menu.selectBackground', self.theme.colors['primary'])
        self.root.option_add('*Menu.selectForeground', self.theme.colors['text'])
    
    def setup_header(self):
        """Create header section with logo and title"""
        header_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # App logo
        logo_label = tk.Label(
            header_frame,
            text="💰",
            font=("Segoe UI Emoji", 36),
            fg=self.theme.colors['primary'],
            bg=self.theme.colors['background']
        )
        logo_label.pack(side="left", padx=(0, 10))
        
        # Title and subtitle container
        title_container = ttk.Frame(header_frame, style="Main.TFrame")
        title_container.pack(side="left", fill="y")
        
        # App title
        title_label = ttk.Label(
            title_container,
            text="Personal Finance Tracker",
            style="Header.TLabel"
        )
        title_label.pack(anchor="w")
        
        # App subtitle
        subtitle_label = ttk.Label(
            title_container,
            text="Track your finances with ease",
            font=("Inter", 14),
            foreground=self.theme.colors['text_secondary'],
            background=self.theme.colors['background']
        )
        subtitle_label.pack(anchor="w")
    
    def setup_balance_section(self):
        """Create balance display section"""
        balance_frame = ttk.Frame(self.main_container, style="Card.TFrame")
        balance_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Add padding frame
        inner_frame = ttk.Frame(balance_frame, style="Card.TFrame", padding=20)
        inner_frame.pack(fill="both", expand=True)
        
        # Configure columns for even spacing
        for i in range(6):
            inner_frame.columnconfigure(i, weight=1)
        
        # Total Income with icon
        income_frame = ttk.Frame(inner_frame, style="Card.TFrame")
        income_frame.grid(row=0, column=0, columnspan=2, padx=10, sticky="ew")
        tk.Label(
            income_frame,
            text="📈",
            font=("Segoe UI Emoji", 24),
            fg=self.theme.colors['success'],
            bg=self.theme.colors['card_bg']
        ).pack(side="left", padx=5)
        ttk.Label(income_frame, text="Total Income", style="Balance.TLabel").pack(side="left")
        self.income_label = ttk.Label(income_frame, text="$0.00", style="PositiveBalance.TLabel")
        self.income_label.pack(side="right", padx=10)
        
        # Total Expenses with icon
        expense_frame = ttk.Frame(inner_frame, style="Card.TFrame")
        expense_frame.grid(row=0, column=2, columnspan=2, padx=10, sticky="ew")
        tk.Label(
            expense_frame,
            text="📉",
            font=("Segoe UI Emoji", 24),
            fg=self.theme.colors['warning'],
            bg=self.theme.colors['card_bg']
        ).pack(side="left", padx=5)
        ttk.Label(expense_frame, text="Total Expenses", style="Balance.TLabel").pack(side="left")
        self.expense_label = ttk.Label(expense_frame, text="$0.00", style="NegativeBalance.TLabel")
        self.expense_label.pack(side="right", padx=10)
        
        # Net Balance with icon
        net_frame = ttk.Frame(inner_frame, style="Card.TFrame")
        net_frame.grid(row=0, column=4, columnspan=2, padx=10, sticky="ew")
        tk.Label(
            net_frame,
            text="💰",
            font=("Segoe UI Emoji", 24),
            fg=self.theme.colors['primary'],
            bg=self.theme.colors['card_bg']
        ).pack(side="left", padx=5)
        ttk.Label(net_frame, text="Net Balance", style="Balance.TLabel").pack(side="left")
        self.balance_label = ttk.Label(net_frame, text="$0.00", style="PositiveBalance.TLabel")
        self.balance_label.pack(side="right", padx=10)
    
    def setup_main_content(self):
        """Setup main content area with transaction input and lists"""
        # Left column: Transaction input and list
        left_frame = ttk.Frame(self.main_container, style="Card.TFrame")
        left_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        
        # Add padding frame
        left_content = ttk.Frame(left_frame, style="Card.TFrame", padding=20)
        left_content.pack(fill="both", expand=True)
        
        # Initialize transaction components
        self.transaction_input = TransactionInput(left_content, self.handle_transaction_added)
        self.transaction_list = TransactionList(left_content)
        
        # Right column: Charts
        right_frame = ttk.Frame(self.main_container, style="Card.TFrame")
        right_frame.grid(row=2, column=1, sticky="nsew")
        
        # Add padding frame
        right_content = ttk.Frame(right_frame, style="Card.TFrame", padding=20)
        right_content.pack(fill="both", expand=True)
        
        # Initialize charts
        self.charts = FinancialCharts(right_content, self.theme.colors)
    
    def handle_transaction_added(self, transaction):
        """Handle new transaction added"""
        # Add to transactions list
        self.transactions.append(transaction)
        
        # Update totals with animation
        if transaction['type'] == "Income":
            ValueAnimator.animate_value_change(
                self.root,
                self.income_label,
                self.total_income,
                self.total_income + transaction['amount']
            )
            self.total_income += transaction['amount']
        else:
            ValueAnimator.animate_value_change(
                self.root,
                self.expense_label,
                self.total_expenses,
                self.total_expenses + transaction['amount']
            )
            self.total_expenses += transaction['amount']
        
        # Update net balance
        net_balance = self.total_income - self.total_expenses
        ValueAnimator.animate_value_change(
            self.root,
            self.balance_label,
            net_balance - transaction['amount'] if transaction['type'] == "Expense" else net_balance,
            net_balance
        )
        
        # Update transaction list
        self.transaction_list.add_transaction(transaction)
        
        # Update charts
        self.charts.update_charts(self.transaction_list.get_all_transactions())

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceTracker(root)
    root.mainloop()