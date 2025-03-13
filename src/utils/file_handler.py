import json
import os
from tkinter import filedialog, messagebox
import pickle

class FileHandler:
    """Utility class for handling file operations (save/load)"""
    
    @staticmethod
    def save_data(data, default_filename="finance_data.json"):
        """
        Save financial data to a JSON file
        
        Args:
            data (dict): The financial data to save
            default_filename (str): Default filename to suggest
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Ask user where to save the file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=default_filename
            )
            
            # If user cancels the save dialog
            if not file_path:
                return False
            
            # Save data to the selected file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            
            return True
        
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving: {str(e)}")
            return False
    
    @staticmethod
    def load_data():
        """
        Load financial data from a JSON file
        
        Returns:
            dict: The loaded financial data or None if loading failed
        """
        try:
            # Ask user which file to load
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            # If user cancels the open dialog
            if not file_path:
                return None
            
            # Load data from the selected file
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            return data
        
        except json.JSONDecodeError:
            messagebox.showerror("Load Error", "The selected file is not a valid JSON file.")
            return None
        
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading: {str(e)}")
            return None
    
    @staticmethod
    def export_to_csv(data, default_filename="finance_data.csv"):
        """
        Export financial data to a CSV file
        
        Args:
            data (list): List of transaction dictionaries
            default_filename (str): Default filename to suggest
        
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            import csv
            
            # Ask user where to save the CSV file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=default_filename
            )
            
            # If user cancels the save dialog
            if not file_path:
                return False
            
            # Define CSV headers based on transaction data structure
            headers = ["date", "description", "amount", "type"]
            
            # Write data to CSV file
            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                for transaction in data:
                    writer.writerow(transaction)
            
            return True
            
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting: {str(e)}")
            return False
    
    @staticmethod
    def import_from_csv():
        """
        Import financial data from a CSV file
        
        Returns:
            list: List of transaction dictionaries or None if import failed
        """
        try:
            import csv
            
            # Ask user which CSV file to import
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            # If user cancels the open dialog
            if not file_path:
                return None
            
            transactions = []
            
            # Read data from CSV file
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert amount to float
                    row['amount'] = float(row['amount'])
                    transactions.append(row)
            
            return transactions
            
        except Exception as e:
            messagebox.showerror("Import Error", f"An error occurred while importing: {str(e)}")
            return None