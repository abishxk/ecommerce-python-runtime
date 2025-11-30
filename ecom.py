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
    n = int(input("> "))
    if n == 1:
        login()
    elif n == 2:
        signup_roles()
    else:
        print("Invalid input... Try again :(")
        welcome()


def signup_roles():
    print("*****************************************************")
    print("1 - Customer")
    print("2 - Product Team")
    print("3 - Order Module Team")
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

def shop():
    print("*****************************************************")
    filename = "products.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []

    if products:
        print(f"{'S.NO':<10}{'NAME':<15}{'PRICE':<10}{'QTY':<10}{'TYPE':<15}")
        print("-----------------------------------------------------")
        x = 1
        prodsidx = []
        for prod in products:
            print(f"{x:<10}{prod['name']:<15}{prod['price']:<10}{prod['quantity']:<10}{prod['type']:<15}")
            prodsidx.append(x)
            x += 1
        z = choose_product(prodsidx)
        chosen_product = products[z-1]
        print(f"\n****** you chose : {products[z-1]['name']} ******\n")
        add_to_cart(z,chosen_product)


    else:
        print("No products available at the moment...")

def choose_product(prodsidx):
    print("*****************************************************")
    ch = int(input("Enter Serial number(S.NO) of the product : "))
    if ch in prodsidx:
        return ch

    else:
        print("Product with given serial number doesnt exist... Try again :(")
        choose_product(prodsidx)

def prod_search():
    print("*****************************************************")
    name = input("Enter a product name to search : ")
    filename = "products.json"

    # Load existing data
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []
    result = []
    resultidx = []
    y = 1
    print("************************Matching Products****************************")
    for p in products:
        if name in p["name"]:
            result.append(p)
            resultidx.append(y)
            y+=1

    if not result:
        print("No matching products found!")
        prod_search()
    else:
        print(f"{'S.NO':<10}{'NAME':<15}{'PRICE':<10}{'QTY':<10}{'TYPE':<15}")
        for prod, idx in zip(result, resultidx):
            print(f"{y:<10}{prod['name']:<15}{prod['price']:<10}{prod['quantity']:<10}{prod['type']:<15}")
            z = choose_product(resultidx)
            chosen_product = result[z - 1]
            print(f"\n****** you chose : {result[z - 1]['name']} ******\n")
            add_to_cart(z, chosen_product)

def quantity(q):
    print("*****************************************************")
    qty = int(input("Enter quantity of the product : "))
    if qty <= q:
        return qty
    else:
        print("Input greater than available quantity... Try again :(")
        quantity(q)

def add_to_cart(z,chosen_product):
    print("*****************************************************")
    print(f"{'NAME':<15}{'PRICE':<10}{'QTY':<10}")
    print(f"{chosen_product['name']:<15}{chosen_product['price']:<10}{chosen_product['quantity']:<10}")
    qty = quantity(chosen_product['quantity'])
    filename = "cart.json"

    temp_prod = chosen_product
    temp_prod['quantity'] = qty

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                carts = json.load(f)
            except json.JSONDecodeError:
                carts = []
    else:
        carts = []

    email = s.logged_in_user

    user_exists = False

    for i in carts:
        if i["email"] == email :
            i["cart"].append(temp_prod)
            user_exists = True
            break
        else:
            continue
    if not user_exists:
        carts .append({
            "email" : email,
            "cart" : [temp_prod]
        })

    with open(filename, "w") as f:
        json.dump(carts,f,indent=4)

    if os.path.exists("products.json"):
        with open("products.json", "r") as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []

    for prods in products:
        if temp_prod['name'] == prods['name']:
            prods['quantity'] -= temp_prod['quantity']
            break

    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

    print(f"\n*** {temp_prod['name']} has been added to cart! :) *** \n")




def view_cart():
    print("*****************************************************")
    filename = "cart.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                carts = json.load(f)
            except json.JSONDecodeError:
                carts = []
    else:
        carts = []

    if carts:
        grand_total = 0
        for i in carts:
            print(f"{'NAME':<15}{'PRICE':<10}{'QTY':<10}{'TOTAL'}")
            for item in i['cart']:
                total = item['price'] * item['quantity']
                grand_total += total
                print(f"{item['name']:<15}{item['price']:<10}{item['quantity']:<10}{total}")
            print("-----------------------------------------")
            print(f"{'GRAND TOTAL':<35}{grand_total}")
    else:
        print("cart is empty...")
        return


if __name__ == "__main__":
    welcome()
    print("ok")


