import os
import session as s
import customer as cu
import json
import product_team as pt
import order_module as om


def welcome():
    print("*****************************************************")
    print("1 - Login")
    print("2 - Signup")
    print("3 - Exit")
    n = int(input("> "))
    if n == 1:
        login()
    elif n == 2:
        signup_roles()
    elif n == 3 :
        return
    else:
        print("Invalid input... Try again :(")
        welcome()


def signup_roles():
    print("*****************************************************")
    print("1 - Customer")
    print("2 - Product Team")
    print("3 - Order Module Team")
    print("4 - Back")
    n = int(input("> "))
    if n == 1:
        cu.customer_signup()
        login()
    elif n == 2:
        pt.product_team_signup()
        login()
    elif n == 3:
        om.order_module_signup()
        login()
    elif n == 4:
        welcome()
    else:
        print("Invalid input... Try again")
        signup_roles()


def login():
    print("*****************************************************")
    mail = input("Enter your mail: ")
    password = input("Enter your password: ")

    filename = "users.json"

    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            print("users.json is corrupted.")
            return
    else:
        return

    for c in users:
        if c["email"] == mail and c["password"] == password:
            print("\n*** Login successful! ***\n")
            s.logged_in_user = mail

            role = c["role"]
            if role == "CUSTOMER":
                cu.customer_menu()
            elif role == "PRODUCT_TEAM":
                pt.product_team_menu()
            elif role == "ORDER_TEAM":
                om.order_module_team_menu()

            return

    print("Invalid cred... Try again")
    login()


if __name__ == "__main__":
    welcome()
    print("*****************************************************")
    print("Thank you for using cheee shop... :)")


