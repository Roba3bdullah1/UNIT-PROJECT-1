import json 
from datetime import datetime
import os 
import openai
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai.api_key= os.getenv("OPENAI_API_KEY")

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
        username = input("Enter an username: ").strip()
        if not username:
            print("Username cannot be empty.")
        if username in self.users:
            print("Username already exists.")
            return False
        
        password = input("Enter a passeord: ").strip()
        if len(password) < 4:
            print("Password must be at least 4 characters.")
            return False

        self.users[username] = password
        self.save_users()
        print("Registation successful!")
        return True

    def login_user(self):
        username = input("Enter an username: ").strip()
        password = input("Enter a passeord: ").strip()

        if not username or not password:
            print("Username and password cannot be empty.")
            return False

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
            "amount" : amount,
            "category" : category,
            "date" : datetime.now().isoformat()
        }

        self.income.append(income_list)
        self.save_data()

    def add_expense(self,amount:float, category:str):
        expense_list = {
            "amount" : amount,
            "category" : category,
            "date" : datetime.now().isoformat()

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
        total_income = self.get_total_income()
        total_expense = self.get_total_expense()
        balance = self.get_balance()
        
        income_by_category = self.category(self.income)
        expense_by_category = self.category(self.expenses)

    
        expense_percentage = {}
        if total_expense > 0:
            for category, amount in expense_by_category.items():
                expense_percentage[category] = (amount / total_expense) * 100
        
        return {
            "total_income" : self.get_total_income(),
            "total_expenses" : self.get_total_expense(),
            "balance" : self.get_balance(),
            "by_income" : self.category(self.income),
            "by_expense": self.category(self.expenses),
            "expenses_percentage": expense_percentage
            
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
            "income" : self.income,
            "expenses" : self.expenses,
            "goal_amount" : self.goal_amount,
            "goal_deadline" : self.goal_deadline.isoformat() if self.goal_deadline else None

        }

        with open(filename,"w") as f:
            json.dump(data,f,indent=4)

    def update_category(self):
        print("\nChoose the type of category you want to update:")
        print("1. Income Category")
        print("2. Expense Category")
        
        category_type = input("Enter the number (1 or 2): ")

        if category_type == "1":
            self.update_income()
        elif category_type == "2":
            self.update_expense()
        else:
            print("Invalid choice. Please try again.")
    
    def update_income(self):
        print("\n--- Income Categories ---")
        for i, income in enumerate(self.income, 1):
            print(f"{i}. Category: {income['category']} | Amount: {income['amount']} | Date: {income['date']}")
        try:
            category_number = int(input("\nEnter the number of the income category to update: "))
            if category_number < 1 or category_number > len(self.income):
                print("Invalid choice. Please try again.")
                return

           
            selected_income = self.income[category_number - 1]
            new_category = input(f"Enter new category name (current: {selected_income['category']}): ")
            new_amount = float(input(f"Enter new amount (current: {selected_income['amount']}): "))
            selected_income['category'] = new_category if new_category else selected_income['category']
            selected_income['amount'] = new_amount if new_amount else selected_income['amount']
            print(f"Income category updated successfully: {selected_income}")
            self.save_data()

        except ValueError:
            print("Invalid input. Please try again.")


    def update_expense(self):
        print("\n--- Expense Categories ---")
        for i, expense in enumerate(self.expenses, 1):
            print(f"{i}. Category: {expense['category']} | Amount: {expense['amount']} | Date: {expense['date']}")
        try:
            category_number = int(input("\nEnter the number of the expense category to update: "))
            if category_number < 1 or category_number > len(self.expenses):
                print("Invalid choice. Please try again.")
                return

            selected_expense = self.expenses[category_number - 1]
            new_category = input(f"Enter new category name (current: {selected_expense['category']}): ")
            new_amount = float(input(f"Enter new amount (current: {selected_expense['amount']}): "))
            selected_expense['category'] = new_category if new_category else selected_expense['category']
            selected_expense['amount'] = new_amount if new_amount else selected_expense['amount']
            print(f"Expense category updated successfully: {selected_expense}")
            self.save_data()

        except ValueError:
            print("Invalid input. Please try again.")        


    
    def check_notifications(self):
        notifications = []
        balance = self.get_balance()

        if balance < 100:
            notifications.append("Your balance is low. saving more.")
        if self.get_total_expense() > self.get_total_income():
            notifications.append("You are spending more than your income. Review your expenses.")
        if not self.income and not self.expenses:
            notifications.append("No income or expenses recorded yet. ")
        if balance > self.get_total_expense():
            notifications.append("You have a surplus! You can afford to spend more or save.")
        if self.goal_deadline and datetime.now() > self.goal_deadline:
            if self.get_balance() < self.goal_amount:
                notifications.append(f"You missed your goal! Deadline: {self.goal_deadline} | Goal: {self.goal_amount}")
            else:
                notifications.append(f"Congratulations! You met your goal! Deadline: {self.goal_deadline} | Goal: {self.goal_amount}")

        if self.goal_amount and balance < self.goal_amount:
            remaining = self.goal_amount - balance
            notifications.append(f"You are {remaining:.2f} away from your goal! Keep going.")

        if notifications:
            print("\n--- Notifications ---")
            for i in notifications:
                print("-",i)
        else:
            print("NO notifications")

        
    def set_goal(self):
        try:
            print("\n--- Set Goal ---")
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
        remaining = balance - self.goal_amount 
        days_left = (self.goal_deadline - datetime.now()).days

        progress = (balance / self.goal_amount) * 100
        progress=min(progress,100)

        print("\n--- Goal Progress ---")
        with tqdm(total=100,desc="Progress", ncols=100) as pbar:
            pbar.update(int(progress))

        print(f"Goal : {self.goal_amount} - Current balance: {balance}")
        print(f"Progress: {progress:.2f}%")
        print(f"Days left : {days_left} days")

        if progress == 100:
            print("Congratulations! You've reached your goal!")
        elif balance > self.goal_amount:
            print("You have surpassed your goal, Great job!")
        elif remaining > 0:
            print(f"You're {remaining:.2f} away from reaching your goal.")
        else:
            print("You are on track, keep going!")

    

    def get_chatgpt_suggestions(self):
        print("\n--- Getting smart suggestions from ChatGPT ---")
        prompt = (f"""
            I am using a personal budget calculator . Here is my financial data:
            - Total income: {self.get_total_income()}
            - Total expenses: {self.get_total_expense()}
            - Current balance: {self.get_balance()}
            - Income categories: {self.category(self.income)}
            - Expense categories: {self.category(self.expenses)}
            Based on my data, please give me personalized financial advice to improve my savings, reduce unnecessary expenses, and plan for financial goals.
                """  ) 
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            
            suggestions = response['choices'][0]['message']['content']
            return suggestions

        except Exception as e:
            return f"Error: {e}"


    
        

        
