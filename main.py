from user import User
from user import MangeUser


print("-"*35)
print("Welcome to Smart Budget Calculator!")
print("-"*35)


def add_income(user):
    try:
        amount = float(input("Enter income amount:"))
        category = input("Enter income category:")

        if not category:
            category = ""

        user.add_income(amount,category)
        print(f"Income of {amount} added to category {category}")

    except ValueError:
        print("Invalid amount. please enter number.")


def add_expense(user):
    try:
        amount = float(input("Enter expense amount:"))
        category = input("Enter expense category:")
        if not category:
            category = ""

        user.add_expense(amount,category)
        print(f"Expense of {amount} added to category {category}")

    except ValueError:
        print("Invalid amount. please enter number.")


def show_summary(user):
    summary = user.get_summary()
    print("--- BUDGET Summary ---")
    print(f"Total Income: {summary['total_income']}")
    print(f"Total Expenses : {summary['total_expenses']}")
    print(f"Balance : {summary['balance']}")

    print("Income by category:")
    for category,amount in summary['by_income'].items():
        print(f" - {category}: {amount}")

    print("Expenses by category:")
    for category,amount in summary['by_expense'].items():
        print(f" - {category}: {amount}")


user = MangeUser()

while True:
    print('''
    
    Choose an options :
        1. Sign Up.
        2. Log In.
        3. Exit.

        ''')
    
    user_input=input("Your choice :")
    if user_input == "1":
        user.register_user()
        
    elif user_input == "2":
        success = user.login_user()
        if success:
            current_user = user.get_current_user()

            while True:
                print("-"*40)
                print('''                  
                Choose one :
                    1. Add income.
                    2. Add expense.
                    3. View a budget summary.
                    4. View category details.
                    5. Update category details.
                    6. Track goal.
                    7. View notifications.
                    8. Import your data.
                    9. Log out.
                            ''')
                print("-"*40)

                user_input2 = input("Your choice:")
                if user_input2 == "1":
                    add_income(current_user)
                elif user_input2 == "2":
                    pass
                elif user_input2 == "3":
                    pass
                elif user_input2 == "4":
                    pass
                elif user_input2== "5":
                    pass
                elif user_input2 == "6":
                    pass
                elif user_input2 == "7":
                    pass
                elif user_input2 == "8":
                    pass
                elif user_input2 == "9":
                    print("Log out...")
                    break
                    
                else:
                    print("Invalid choice. Try again.")
      
    elif user_input == "3":
        print("Goodbye..")
        break
    else:
        print("Invalid choice.")


