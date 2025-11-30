import json
import ecom as ec
import os

def product_team_signup():
    print("*****************************************************")
    pname = input("Enter your name: ")
    pmail = input("Enter your email: ")
    ppass = input("Enter your password: ")

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
        "name": pname,
        "email": pmail,
        "password": ppass,
        "role": "PRODUCT_TEAM"
    }

    users.append(new_user)

    with open(filename, "w") as f:
        json.dump(users, f, indent=4)

    print("User added!")
    print("Please login now...")
    return

def add_product():
    print("*****************************************************")
    prname = input("Enter product name : ")
    prprice = float(input("Enter product price : "))
    prqty = int(input("Enter product quantity : "))
    prtype = input("Enter product type : ")

    filename = "products.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []

    new_prod = {
        "name": prname,
        "price": prprice,
        "quantity": prqty,
        "type": prtype
    }

    products.append(new_prod)

    with open(filename, "w") as f:
        json.dump(products, f, indent=4)

    print("Product added!")

def product_team_menu():
    print("*****************************************************")
    print('''
            ******Product Team Menu******
            1 - Add Product
            ''')
    n = int(input())
    if n == 1:
        add_product()
    else:
        print("Invalid Input... Try again")
        product_team_menu()