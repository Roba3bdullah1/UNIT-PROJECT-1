import os
from user import User
from user import MangeUser
from colorama import init, Fore, Back, Style
init(autoreset=True)

print("-"*35)
print(Fore.CYAN + "Welcome to Smart Budget Calculator!")
print("-"*35)

def add_income(user):
    ''' Prompts the user to enter income amount and category, then adds the income to user's data'''
    flag = True
    while flag:
        try:
            amount = float(input("Enter income amount : "))
            category = input("Enter income category : ")
            if not category:
                category = ""
            user.add_income(amount,category)
            print( Fore.GREEN +f"Income of {amount} added to category {category}")
            income2 = input(" Do you want to add anather income (y/n): ").strip().lower()
            if income2 == "n":
                flag = False
        except ValueError:
            print("Invalid amount. please enter number.")


def add_expense(user):
    ''' Prompts the user to enter expense amount and category, then adds the expense to user's data '''
    flag = True
    while flag:
        try:
            amount = float(input("Enter expense amount:"))
            category = input("Enter expense category:")
            if not category:
                category = ""

            user.add_expense(amount,category)
            print(Fore.GREEN + f"Expense of {amount} added to category {category}")
            expense2 = input(" Do you want to add anather expense (y/n): ").strip().lower()
            if expense2 == "n":
                flag = False
        except ValueError:
            print("Invalid amount. please enter number.")


def show_summary(user):
    ''' Displays the total income, expenses, balance '''
    summary = user.get_summary()
    print("\n--------- BUDGET SUMMARY ---------")
    print(Fore.LIGHTGREEN_EX + f"- Total Income : {summary.get('total_income', 0)}")
    print(Fore.LIGHTRED_EX + f"- Total Expenses : {summary.get('total_expenses', 0)}")
    print(Fore.LIGHTYELLOW_EX + f"- Balance : {summary.get('balance', 0)} " )

    print("\nIncome by category:")
    for category,amount in summary['by_income'].items():
        print(f" - {category}: {amount}")

    print("\nExpenses by category ordered by highest spending:")
    if summary['total_expenses'] > 0:
        expenses_sorted = sorted(summary['by_expense'].items(), key=lambda x: x[1], reverse=True)
        for category,amount in expenses_sorted:
            percentage = summary["expenses_percentage"].get(category, 0)
            print(f" - {category}: {amount} | {percentage:.2f}%")

    else:
        print("No expenses recorded.")



user = MangeUser()

try:
    while True:
        print('''
Choose an option:
1. Sign Up
2. Log In
3. Exit
        ''')

        user_input = input("Your choice: ").strip()

        if user_input == "1":
            user.register_user()

        elif user_input == "2":
            success = False
            while not success:
                success = user.login_user()
                if not success:
                    
                    break
            
                current_user = user.get_current_user()
                current_user.load_budget()

                while True:
                    print("-" * 35)
                    print('''Choose one:
1. Add Income
2. Add Expense
3. View Budget Summary
4. Update Categories
5. Manage Financial Goals
6. View Notifications
7. Get Smart Suggestions
8. Log out
                    ''')
                    print("-" * 35)

                    user_input2 = input("Your choice: ").strip()

                    if user_input2 == "1":
                        add_income(current_user)
                    elif user_input2 == "2":
                        add_expense(current_user)
                    elif user_input2 == "3":
                        show_summary(current_user)
                    elif user_input2 == "4":
                        current_user.update_category()
                    elif user_input2 == "5":
                        print('''
1. Set new goal
2. Track your goal
                        ''')
                        print("-" * 35)
                        goal_choice = input("Your choice: ").strip()
                        if goal_choice == "1":
                            current_user.set_goal()
                        elif goal_choice == "2":
                            current_user.track_goal()
                        else:
                            print("Invalid choice")

                    elif user_input2 == "6":
                        current_user.check_notifications()
                    elif user_input2 == "7":
                        print(current_user.get_chatgpt_suggestions())
                    elif user_input2 == "8":
                        print("Log out...")
                        current_user.save_data()
                        break
                    else:
                        print("Invalid choice. Try again.")

        elif user_input == "3":
            print(Fore.CYAN + "\nThank you for using Smart Budget Calculator. ")
            print(Fore.CYAN + "Goodbye..")
            break
        else:
            print("Invalid choice. \n")

except Exception as e:
    print(f"Error: {e}")