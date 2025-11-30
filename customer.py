import json
import os
import session as s

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
    5 - Exit
    ''')
    n = int(input("> "))
    if n == 1:
        shop()
    elif n == 2:
        prod_search()
    elif n == 3:
        view_cart()
    elif n == 5:
        return
    else:
        print("Invalid Input... Try again :(")
        customer_menu()

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
        print("*****************************************************")
        z = choose_product(prodsidx,x)
        if z == 0:
            return customer_menu()
        else:
            chosen_product = products[z - 1]
            print(f"\n****** you chose : {products[z - 1]['name']} ******\n")
            add_to_cart(chosen_product)


    else:
        print("No products available at the moment...")

def choose_product(prodsidx,x):
    print(f'''Enter serial number(S.NO) of the product
    (or {x} to go back): ''')
    ch = int(input("> "))
    if ch in prodsidx:
        return ch
    elif ch == x:
        return 0
    else:
        print("Product with given serial number doesnt exist... Try again :(")
        choose_product(prodsidx,x)

def prod_search():
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

    if not products:
        print("No products to search...")
        return customer_menu()

    name = input("Enter a product name to search (or press 'ENTER' to go back) : ")
    if name == "":
        return customer_menu()
    else:
        result = []
        resultidx = []
        y = 1
        print("************************Matching Products****************************")
        for p in products:
            if name in p["name"]:
                result.append(p)
                resultidx.append(y)
                y += 1

        if not result:
            print("No matching products found!")
            return prod_search()
        else:
            print(f"{'S.NO':<10}{'NAME':<15}{'PRICE':<10}{'QTY':<10}{'TYPE':<15}")
            for prod, idx in zip(result, resultidx):
                print(f"{idx:<10}{prod['name']:<15}{prod['price']:<10}{prod['quantity']:<10}{prod['type']:<15}")
            print("*********************************************************************")
            z = choose_product(resultidx, y)
            if z == 0:
                return customer_menu()
            else:
                chosen_product = result[z - 1]
                print(f"\n****** you chose : {chosen_product['name']} ******\n")
                add_to_cart(chosen_product)

def quantity(available):
    print("*****************************************************")
    print('''Enter quantity of the product : 
    (or 0 to go back)''')
    qty = int(input("> "))
    if qty == 0:
        return shop()
    elif qty <= available:
        return qty
    else:
        return 0

def add_to_cart(chosen_product):
    print("*****************************************************")
    print(f"{'NAME':<15}{'PRICE':<10}{'QTY':<10}")
    print(f"{chosen_product['name']:<15}{chosen_product['price']:<10}{chosen_product['quantity']:<10}")
    qty = quantity(chosen_product['quantity'])
    if qty == 0:
        print("Input greater than available quantity... Try again :(")
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

    for cart in carts:
        if cart["email"] == email:
            cart["cart"].append(temp_prod)
            user_exists = True
            break

    if not user_exists:
        carts.append({
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
    return customer_menu()


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

    user_found = False

    for user_cart in carts:
        if user_cart["email"] == s.logged_in_user:
            user_found = True
            grand_total = 0

            print(f"{'NAME':<15}{'PRICE':<10}{'QTY':<10}{'TOTAL'}")

            for prod in user_cart['cart']:
                total = prod['price'] * prod['quantity']
                grand_total += total
                print(f"{prod['name']:<15}{prod['price']:<10}{prod['quantity']:<10}{total}")

            print("-----------------------------------------")
            print(f"{'GRAND TOTAL':<35}{grand_total}")

            print('''
            1 - Proceed to check out
            2 - Back
            ''')
            n = int(input("> "))

            if n == 1:
                print("check out page")
            else:
                return customer_menu()


    if not user_found:
        print("Cart is empty...")
        return customer_menu()

