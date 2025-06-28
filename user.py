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
            json.dump(self.users,f)


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
            print(f"Hello , {username}!")
            self.logged_in_user = username
            return True
        else:
            print ("Invaild username or password")
            return False
    
class User:

    def __init__(self,username:str):
        self.username = username
        self.income = []
        self.expenses = []

    def add_income(self,amount:float, category:str):
        income_list = {
            "amount": amount,
            "category": category,
            "date": datetime.now()

        }

        self.income.append(income_list)
        self.save_data()

    def add_expense(self,amount:float, category:str):
        expense_list = {
            "amount": amount,
            "category": category,
            "date": datetime.now()

        }

        self.add_expense.append(expense_list)
        self.save_data()

    def get_total_income(self):
        return sum(item["amount"] for item in self.income)
    
    def get_total_expense(self):
        return sum(item["amount"] for item in self.expenses)
    
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





 


  

