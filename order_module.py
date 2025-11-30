import json
import ecom as ec
import os

def order_module_signup():
    print("*****************************************************")
    oname = input("Enter your name: ")
    omail = input("Enter your email: ")
    opass = input("Enter your password: ")

    filename = "users.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    new_user = {
        "name": oname,
        "email": omail,
        "password": opass,
        "role": "ORDER_TEAM"
    }

    users.append(new_user)

    with open(filename, "w") as f:
        json.dump(users, f, indent=4)

    print("User added!")
    print("Please login now...")
    return

def order_module_team_menu():
    print("***********************")
    print("Order team menu here")