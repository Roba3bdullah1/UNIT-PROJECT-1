import json 
import os
from datetime import datetime


class MangeUser:

    def __init__(self,filename="users.json"):
        self.filename= filename
        self.users = self.load_users()
        self.logged_in_user = None
        self.user_objects = {}

    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename,"r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.filename,"w") as f:
            json.dump(self.users, f, indent=4)


    def register_user(self):
        username = input("Enter an username: ")
        password = input("Enter a passeord: ")

        if username in self.users:
            print("Username already exists.")
            return False

        self.users[username] = password
        self.save_users()
        print("Registation successful!")
        return True

    def login_user(self):
        username = input("Enter an username: ")
        password = input("Enter a passeord: ")

        if username in self.users and self.users[username] == password:
            print(f"\nHello, {username}!")
            self.logged_in_user = username
            return True
        else:
            print ("Invaild username or password")
            return False
    
    def get_current_user(self):
        if not self.logged_in_user:
            return None
        if self.logged_in_user not in self.user_objects:
            self.user_objects[self.logged_in_user] = User(self.logged_in_user)
        return self.user_objects[self.logged_in_user]


class User:

    def __init__(self,username:str):
        self.username = username
        self.income = []
        self.expenses = []
        self.goal_amount = None
        self.goal_deadline = None

    def add_income(self,amount:float, category:str):
        income_list = {
            "amount": amount,
            "category": category,
            "date": datetime.now().isoformat()

        }

        self.income.append(income_list)
        self.save_data()

    def add_expense(self,amount:float, category:str):
        expense_list = {
            "amount": amount,
            "category": category,
            "date": datetime.now().isoformat()

        }

        self.expenses.append(expense_list)
        self.save_data()

    def get_total_income(self):
        return sum(i["amount"] for i in self.income)
    
    def get_total_expense(self):
        return sum(i["amount"] for i in self.expenses)
    
    def get_balance(self):
        return self.get_total_income() - self.get_total_expense()
    
    def category(self,data_list):
        result = {}
        for i in data_list:
            category = i["category"]
            amount = i["amount"]

            if category in result:
                result[category] += amount
            else:
                result[category] = amount

        return result
    
    def get_summary(self):
        return {
            "total_income": self.get_total_income(),
            "total_expenses" : self.get_total_expense(),
            "balance" : self.get_balance(),
            "by_income" : self.category(self.income),
            "by_expense": self.category(self.expenses),
            
        }
    
    def load_budget(self):
        filename = f"{self.username}_budget.json"
        if os.path.exists(filename):
            with open(filename,"r") as f:
                data = json.load(f)
            self.income=data.get("income",[])
            self.expenses = data.get("expenses",[])
            self.goal_amount= data.get("goal_amount")
            deadline= data.get("goal_deadline")

            if deadline:
                try:
                    self.goal_deadline = datetime.fromisoformat(deadline)
                except ValueError:
                    self.goal_deadline = None
        else:
            self.income= []
            self.expenses = []
            self.goal_amount = None
            self.goal_deadline = None

    def save_data(self):
        filename = f"{self.username}_budget.json"
        data = {
            "income": self.income,
            "expenses":self.expenses,
            "goal_amount": self.goal_amount,
            "goal_deadline": self.goal_deadline.isoformat() if self.goal_deadline else None

        }

        with open(filename,"w") as f:
            json.dump(data,f,indent=4)


    def show_category_details(self):
        print("\n--- Income Details ---")
        if not self.income:
            print("No income record found")
        else:
            for i in self.income:
                category = i.get("category","Uncategorized")
                amount = i.get("amount", 0)
                date = i.get("date", "Unknown")
                print(f"Category: {category} | Amount: {amount:.2f} | Date: {date}")

        print("\n--- Expense Details ---")
        if not self.expenses:
            print("No expense records found.")
        else:
            for i in self.expenses:
                category = i.get("category", "Uncategorized")
                amount = i.get("amount", 0)
                date = i.get("date", "Unknown")
                print(f"Category: {category} | Amount: {amount:.2f} | Date: {date}")

    
    def check_notifications(self):
        notifications = []
        balance = self.get_balance()

        if balance < 100:
            notifications.append("Your balance is low")
        if self.get_total_expense() > self.get_total_income():
            notifications.append(" -ALERTS- You are spending more than your income.")
        if not self.income and not self.expenses:
            print(" -ALERTS- No income or expenses recorded yet. ")

        if notifications:
            print("Notifications")
            for i in notifications:
                print("-",i)
        else:
            print("NO notifications")

        
    def set_goal(self):
        try:
            amount = float(input("Enter your goal amount:"))
            deadline= input("Enter deadline (YYYY-MM-DD):")
            deadline = datetime.fromisoformat(deadline)
            self.goal_deadline = deadline

            self.goal_amount= amount
            self.deadline = deadline
            self.save_data()
            print(f"Goal of {amount} set for {deadline}")
        except ValueError:
            print("Invalid input. Please try again.")


    def track_goal(self):
        if self.goal_amount is None or self.goal_deadline is None:
            print("No goal set yet.")
            return
        balance = self.get_balance()
        remaining = self.goal_amount - balance
        days_left = (self.goal_deadline - datetime.now()).days

        print(f"Goal: {self.goal_amount}")
        print(f"Current balance: {balance}")
        print(f"Days left: {days_left}")

        if remaining <= 0:
            print("Congrates, You reached your goal!") 
        else:
            print(f"You need {remaining} more to reach your goal.")

    def export_data(self, filename=None):
        if filename is None:
            filename = f"{self.username}_budget_export.json"
        
        data = {
            "income": self.income,
            "expenses": self.expenses,
            "goal_amount": self.goal_amount,
            "goal_deadline": self.goal_deadline.isoformat() if self.goal_deadline else None
        }

        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Data exported successfully to {filename}")
        except Exception as e:
            print(f"Failed to export data: {e}")


    
        

        
