import os
from user import User
from user import MangeUser

print("-"*35)
print("Welcome to Smart Budget Calculator!")
print("-"*35)

def add_income(user):
    try:
        amount = float(input("Enter income amount : "))
        category = input("Enter income category : ")

        if not category:
            category = ""

        user.add_income(amount,category)
        print(f"Income of {amount} added to category {category}")

    except ValueError:
        print("Invalid amount. please enter number.")


def add_expense(user):
    flag = True
    while flag:
        try:
            amount = float(input("Enter expense amount:"))
            category = input("Enter expense category:")
            if not category:
                category = ""

            user.add_expense(amount,category)
            print(f"Expense of {amount} added to category {category}")
            another = input("do you want to add anather expense (y/n): ").lower()
            if another == "n":
                flag = False

        except ValueError:
            print("Invalid amount. please enter number.")


def show_summary(user):
    summary = user.get_summary()
    print("--- BUDGET Summary ---")
    print(f"Total Income : {summary.get('total_income', 0)}")
    print(f"Total Expenses : {summary.get('total_expenses', 0)}")
    print(f"Balance : {summary.get('balance', 0)}")

    print("Income by category:")
    for category,amount in summary['by_income'].items():
        print(f" - {category}: {amount}")

    print("Expenses by category:")
    for category,amount in summary['by_expense'].items():
        print(f" - {category}: {amount}")


user = MangeUser()
while True:
    print(''' Choose an options :
    1. Sign Up
    2. Log In
    3. Exit
        ''')
    
    user_input=input("Your choice : ")
    if user_input == "1":
        user.register_user()
        
    elif user_input == "2":
        success = user.login_user()
        if success:
            current_user = user.get_current_user()
            current_user.load_budget()

            while True:
                print("-"*35)
                print(''' Choose one :
        1. Add income
        2. Add expense
        3. View a budget summary
        4. Update category details
        5. Track goal
        6. View notifications
        7. Import your data
        8. Get smart suggestions
        9. Log out ''')
                print("-"*35)

                user_input2 = input("Your choice : ")
                if user_input2 == "1":
                    add_income(current_user)
                elif user_input2 == "2":
                    add_expense(current_user)
                elif user_input2 == "3":
                    show_summary(current_user)
                elif user_input2== "4":
                    print("\n--Update category--")

                elif user_input2 == "5":
                    print(''' 
                    1. Set new goal.
                    2. Track your goal.
                          ''')
                    goal_choies = input("Your choice:")
                    if goal_choies == "1":
                        current_user.set_goal()
                    elif goal_choies == "2":
                        current_user.track_goal()
                    else:
                        print("Invalid choice")     
                elif user_input2 == "6":
                    current_user.check_notifications()
                elif user_input2 == "7":
                    current_user.export_data()
                elif user_input2 == "8":
                    print("\n---Getting smart suggestions from ChatGPT---")
                    print(current_user.get_chatgpt_suggestions())
                elif user_input2 == "9":
                    print("Log out...")
                    current_user.save_data()
                    break    
                else:
                    print("Invalid choice. Try again.")
      
    elif user_input == "3":
        print("Goodbye..")
        break
    else:
        print("Invalid choice.")


