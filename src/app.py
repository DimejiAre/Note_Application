from src.database import Database
from src.models.user import User
import sys

# create database
Database.initialize()

username = input("welcome to Note Application\n\nPlease enter username: ")

user = User.get_by_username(username)

if user is not None:
    print("\nwelcome back {}".format(user.username))
    trials = 0
    while trials < 3:
        password = input("\nEnter your password: ")
        new_user = user.login(username, password)
        if new_user is not None:
            break
        else:
            print("\nincorrect password")
            trials += 1
    else:
        print("Goodbye!!")
        sys.exit()

else:
    print("User does not Exist")
    trials = 0
    while trials < 3:
        password = input("create a password to signup: ")
        password2 = input("Re-type password: ")
        if password == password2:
            user = User.register(username, password)
            break
        else:
            print("Passwords don't match")
            trials += 1
    else:
        print("Goodbye!!")
        sys.exit()


while True:
    answer = input("\nChoose Action: \n1. Read Note\n2. Create Note\n3. Edit Note\n4. Delete Note\n5. Exit\n")

    if answer == "1":
        user.read_data()
    elif answer == "2":
        user.write_data()
    elif answer == "3":
        user.edit_data()
    elif answer == "4":
        user.delete_data()
    elif answer == "5":
        print("Goodbye!")
        sys.exit()
    else:
        print("Invalid Entry")

    while True:
        answer = input("Do you want to perform another action? Y/N: ")

        if answer.strip().lower() == "n":
            print("Thank you for using the application")
            break
        elif answer.strip().lower() == "y":
            break
        else:
            print("invalid input")

    if answer.strip().lower() == "y":
        continue

    break






