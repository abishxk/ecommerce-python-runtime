import json
import os
import ecom as ec

def customer_signup():
    print("*****************************************************")
    cname = input("Enter your name: ")
    cmail = input("Enter your email: ")
    cpass = input("Enter your password: ")

    filename = "users.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
    else:
        users = []

    new_user= {
        "name": cname,
        "email": cmail,
        "password": cpass,
        "role": "CUSTOMER"
    }

    users.append(new_user)

    with open(filename, "w") as f:
        json.dump(users, f, indent=4)

    print("User added!")
    print("Please login now...")
    return


def customer_menu():
    print("*****************************************************")
    print('''
    ******Customer Menu******
    1 - Shop
    2 - Search
    3 - View Cart
    4 - View Order Status
    ''')
    n = int(input(">"))
    if n == 1:
        ec.shop()
    elif n == 2:
        ec.prod_search()
    elif n == 3:
        ec.view_cart()
    else:
        print("Invalid Input... Try again :(")
        customer_menu()

