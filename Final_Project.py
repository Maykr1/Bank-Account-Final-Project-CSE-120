import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import atexit
#pip install Pillow

class BankAccount:  
    def __init__(self, user_id, password, security_pin, bank, balance=0, savings_balance=0):
        self.user_id = user_id
        self.password = password
        self.security_pin = security_pin
        self.bank = bank
        self.balance = balance
        self.savings_balance = savings_balance

    def check_balance(self):
        return self.balance

    def check_savings_balance(self):
        return self.savings_balance

    def deposit(self, amount, account):
        if account.lower() == "checking":
            self.balance += amount
            self.bank.save_accounts() 
        elif account.lower() == "savings":
            self.savings_balance += amount
            self.bank.save_accounts() 

    def withdraw(self, amount, account):
        if account.lower() == "checking" and self.balance >= amount:
            self.balance -= amount
            self.bank.save_accounts() 
            return True
        elif account.lower() == "savings" and self.savings_balance >= amount:
            self.savings_balance -= amount
            self.bank.save_accounts() 
            return True
        else:
            print("Insufficient funds or invalid account")
            return False

    def transfer(self, amount, transfer_from, transfer_to):
        if self.withdraw(amount, transfer_from):
            self.deposit(amount, transfer_to)
            return True
        return False
    

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'password': self.password,
            'security_pin': self.security_pin,
            'balance': self.balance,
            'savings_balance': self.savings_balance
            }

    @classmethod
    def from_dict(cls, data, bank):
        return cls(
            user_id=data['user_id'],
            password=data['password'],
            security_pin=data['security_pin'],
            bank=bank,
            balance=data.get('balance', 0),
            savings_balance=data.get('savings_balance', 0)
        )

class Bank:
    def __init__(self):
        self.accounts = {}
        self.current_user = None
        self.load_accounts()
        atexit.register(self.save_accounts)

    def save_accounts(self):
        with open('data.json', 'w') as file:
            json.dump({user_id: account.to_dict() for user_id, account in self.accounts.items()}, file)
#User can use this to save data into their bank account of choosing
   
    def load_accounts(self):
        try:
            with open('data.json', 'r') as file:
                accounts_data = json.load(file)
            for user_id, account_data in accounts_data.items():
                self.accounts[user_id] = BankAccount.from_dict(account_data, self)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def create_account(self, user_id, password, security_pin): 
        # Check if the account already exists in the loaded accounts
        if user_id in self.accounts:
            print("Account Already Exists")
            return False
        else:
            self.accounts[user_id] = BankAccount(user_id, password, security_pin, self)
            self.save_accounts()
            print("Account Created Successfully")
            return True

    def login(self, user_id, password):
        if user_id in self.accounts and self.accounts[user_id].password == password:
            self.current_user = self.accounts[user_id]
            print("Login Successful")
            return True
        else:
            print("Invalid User ID or Password")
            return False
#else if function for user if the person forgot their username or password
    def forgot_password(self, user_id, security_pin):
        if user_id in self.accounts and self.accounts[user_id].security_pin == security_pin:
            print("Your password is:", self.accounts[user_id].password)
        else:
            print("Invalid User ID or Security Pin")

class BankGUI:
    def __init__(self, root):
        self.bank = Bank()
        self.root = root
        self.root.title("F.U. Bank")
        

        self.create_account_frame = None
        self.login_frame = None
        self.customer_portal_frame = None

        self.show_main_menu()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()


    def show_main_menu(self):
        self.clear_frame(self.root)
        self.root.iconphoto(False, tk.PhotoImage(file=r"C:\Users\lolxd\OneDrive\Desktop\Final Project\Main_Federal_Union_Logo.png"))
    
        logo_path = r"C:\Users\lolxd\OneDrive\Desktop\Final Project\Main_Federal_Union_Logo.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((190, 150))
        logo_photo = ImageTk.PhotoImage(logo_image)
    
        # Logo label
        logo_label = tk.Label(self.root, image=logo_photo)
        logo_label.image = logo_photo 
        logo_label.pack(pady=5)
        title_label = tk.Label(self.root, text="Welcome to F.U. Bank", font=('Helvetica', 16), fg="red")
        title_label.pack(pady=10)
        title_label.config(anchor="center")
    
        tk.Label(self.root, text="GET STARTED:", font=('Helvetica', 14), fg='blue').pack(pady=5) 
    
        tk.Button(self.root, text="Create Account", command=self.show_create_account_frame, fg='green').pack(pady=5)
        tk.Button(self.root, text="Login", command=self.show_login_frame, fg='purple').pack(pady=5)
        tk.Button(self.root, text="Forgot Password", command=self.show_forgot_password_frame, fg='orange').pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.destroy, fg='brown').pack(pady=5)

    def show_create_account_frame(self):
        self.clear_frame(self.root)

        tk.Label(self.root, text="Create Account", font=('Helvetica', 16)).pack(pady=10)

        tk.Label(self.root, text="User ID:").pack(pady=5)
        user_id_entry = tk.Entry(self.root, width=30)
        user_id_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*", width=30)
        password_entry.pack(pady=5)

        tk.Label(self.root, text="Security Pin:").pack(pady=5)
        security_pin_entry = tk.Entry(self.root, show="*", width=30)
        security_pin_entry.pack(pady=5)

        tk.Button(self.root, text="Create Account", command=lambda: self.create_account(
            user_id_entry.get(), password_entry.get(), security_pin_entry.get())).pack(pady=10)

        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack(pady=5)

    def create_account(self, user_id, password, security_pin):
        if self.bank.create_account(user_id, password, security_pin):
            messagebox.showinfo("Success", "Account created successfully.")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Account creation failed. User ID already exists.")

    def show_login_frame(self):
        self.clear_frame(self.root)

        tk.Label(self.root, text="Login", font=('Helvetica', 16)).pack(pady=10)

        tk.Label(self.root, text="User ID:").pack(pady=5)
        user_id_entry = tk.Entry(self.root, width=30)
        user_id_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*", width=30)
        password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=lambda: self.login(user_id_entry.get(), password_entry.get())).pack(pady=10)

        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack(pady=5)

    def login(self, user_id, password):
        if self.bank.login(user_id, password):
            messagebox.showinfo("Success", "Login successful.")
            self.show_customer_portal_frame()
        else:
            messagebox.showerror("Error", "Invalid User ID or Password.")

    def show_forgot_password_frame(self):
        self.clear_frame(self.root)

        tk.Label(self.root, text="Forgot Password", font=('Helvetica', 16)).pack(pady=10)

        tk.Label(self.root, text="User ID:").pack(pady=5)
        user_id_entry = tk.Entry(self.root, width=30)
        user_id_entry.pack(pady=5)

        tk.Label(self.root, text="Security Pin:").pack(pady=5)
        security_pin_entry = tk.Entry(self.root, show="*", width=30)
        security_pin_entry.pack(pady=5)

        tk.Button(self.root, text="Retrieve Password", command=lambda: self.retrieve_password(
            user_id_entry.get(), security_pin_entry.get())).pack(pady=10)

        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack(pady=5)

    def retrieve_password(self, user_id, security_pin):
        if user_id in self.bank.accounts and self.bank.accounts[user_id].security_pin == security_pin:
            messagebox.showinfo("Password Retrieval", "Your password is: {}".format(self.bank.accounts[user_id].password))
        else:
            messagebox.showerror("Error", "Invalid User ID or Security Pin.")
        self.show_main_menu()

    def show_customer_portal_frame(self):
        self.clear_frame(self.root)

        tk.Label(self.root, text="Customer Portal", font=('Helvetica', 16)).pack(pady=10)

        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit Funds", command=self.show_deposit_frame).pack(pady=5)
        tk.Button(self.root, text="Withdraw Funds", command=self.show_withdraw_frame).pack(pady=5)
        tk.Button(self.root, text="Transfer Funds", command=self.show_transfer_frame).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def check_balance(self):
        balance = self.bank.current_user.check_balance()
        savings_balance = self.bank.current_user.check_savings_balance()
        messagebox.showinfo("Balance", f"Checking Account Balance: ${balance:.2f}\nSavings Account Balance: ${savings_balance:.2f}")
        self.show_customer_portal_frame()

    def show_deposit_frame(self):
        self.clear_frame(self.root)

        tk.Label(self.root, text="Deposit Funds", font=('Helvetica', 16)).pack(pady=10)

        tk.Label(self.root, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(self.root, width=30)
        amount_entry.pack(pady=5)

        tk.Label(self.root, text="Account (Checking/Savings):").pack(pady=5)
        account_entry = tk.Entry(self.root, width=30)
        account_entry.pack(pady=5)

        tk.Button(self.root, text="Deposit", command=lambda: self.deposit_funds(
            float(amount_entry.get()), account_entry.get())).pack(pady=10)

        tk.Button(self.root, text="Back to Customer Portal", command=self.show_customer_portal_frame).pack(pady=5)

    def deposit_funds(self, amount, account):
        self.bank.current_user.deposit(amount, account)
        messagebox.showinfo("Deposit", f"Deposit of ${amount:.2f} to {account} account was successful.")
        self.show_customer_portal_frame()

    def show_withdraw_frame(self):
        self.clear_frame(self.root)

        tk.Label(self.root, text="Withdraw Funds", font=('Helvetica', 16)).pack(pady=10)

        tk.Label(self.root, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(self.root, width=30)
        amount_entry.pack(pady=5)

        tk.Label(self.root, text="Account (Checking/Savings):").pack(pady=5)
        account_entry = tk.Entry(self.root, width=30)
        account_entry.pack(pady=5)

        tk.Button(self.root, text="Withdraw", command=lambda: self.withdraw_funds(
            float(amount_entry.get()), account_entry.get())).pack(pady=10)

        tk.Button(self.root, text="Back to Customer Portal", command=self.show_customer_portal_frame).pack(pady=5)

    def withdraw_funds(self, amount, account):
        if self.bank.current_user.withdraw(amount, account):
            messagebox.showinfo("Withdrawal", f"Withdrawal of ${amount} from {account} account was successful.")
        else:
            messagebox.showerror("Error", "Insufficient funds or invalid account.")
        self.show_customer_portal_frame()

    def show_transfer_frame(self):
        self.clear_frame(self.root)

        tk.Label(self.root, text="Transfer Funds", font=('Helvetica', 16)).pack(pady=10)

        tk.Label(self.root, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(self.root, width=30)
        amount_entry.pack(pady=5)

        tk.Label(self.root, text="Transfer From (Checking/Savings):").pack(pady=5)
        from_entry = tk.Entry(self.root, width=30)
        from_entry.pack(pady=5)

        tk.Label(self.root, text="Transfer To (Checking/Savings):").pack(pady=5)
        to_entry = tk.Entry(self.root, width=30)
        to_entry.pack(pady=5)

        tk.Button(self.root, text="Transfer", command=lambda: self.transfer_funds(
            float(amount_entry.get()), from_entry.get(), to_entry.get())).pack(pady=10)

        tk.Button(self.root, text="Back to Customer Portal", command=self.show_customer_portal_frame).pack(pady=5)

    def transfer_funds(self, amount, transfer_from, transfer_to):
        if self.bank.current_user.transfer(amount, transfer_from, transfer_to):
            messagebox.showinfo("Transfer", f"Transfer of ${amount} from {transfer_from} account to {transfer_to} account was successful.")
        else:
            messagebox.showerror("Error", "Transfer failed. Insufficient funds or invalid accounts.")
        self.show_customer_portal_frame()

    def logout(self):
        self.bank.current_user = None
        messagebox.showinfo("Logout", "Logged out successfully.")
        self.show_main_menu()

def main():
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()