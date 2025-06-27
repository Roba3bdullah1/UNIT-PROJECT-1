import user
import json

print("-"*40)
print("Welcome to Smart Budget Calculator!")
print("-"*40)

user_input=input(print('''
      
Choose an options :
      1. Sign Up.
      2. Log In.
      3. Exit.

      '''))
while True:
    if user_input == "1":
        user.register_user()
    
    elif user_input == "2":
        success = user.login_user()
        if success:
            print("-"*40)
            user_input2= input('''
                                    
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

        if user_input2 == "1":
            pass
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
            pass
            
    elif user_input == "3":
        print("Goodbye..")
        break
    else:
        print("Invalid choice.")


