import json
import os
import time
import session as s
from datetime import date,timedelta

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
    flag = False
    for cart in carts:
        if cart["email"] == email:
            user_cart = cart["cart"]
            for item in user_cart:
                if item["name"] == temp_prod["name"]:
                    item["quantity"] += temp_prod["quantity"]
                    flag = True
                    user_cart = True
                    break
            if not flag:
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

    # for prods in products:
    #     if temp_prod['name'] == prods['name']:
    #         prods['quantity'] -= temp_prod['quantity']
    #         break

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
            if user_cart["cart"]:
                print(f"{'NAME':<15}{'PRICE':<10}{'QTY':<10}{'TOTAL'}")
                current_user_cart = user_cart['cart']
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
                    checkout(current_user_cart)
                else:
                    return customer_menu()
            else:
                print("Cart is empty...")
                return customer_menu()


    if not user_found:
        print("Cart is empty...")
        return customer_menu()

def checkout(cart):
    filename = "products.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                products = json.load(f)
            except json.JSONDecodeError:
                products = []
    else:
        products = []
    c = 0
    for product in products:
        for prod in cart:
            if product["name"] == prod["name"]:
                if product["quantity"] >= prod["quantity"]:
                    c += 1
    if c == len(cart):
        select_address()
    else:
        print("Some items in the cart are not available...")


def select_address():
    filename = "address.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                addresses = json.load(f)
            except json.JSONDecodeError:
                addresses = []
    else:
        addresses = []

    addressidx = []
    user_address = []
    x = 1
    email = s.logged_in_user
    for address in addresses:
        if email == address["email"]:
            for i in address["address"]:
                addressidx.append(x)
                user_address.append(i)
                x += 1
    x = 1
    if user_address:
        print("\t******* Your Saved Addresses *******")
        for address in user_address:
            print(f"""
    ------------------------------------------------------------
    ADDRESS #{x}
    Name       : {address['name']}
    Address    : {address['first_line']}
                 {address['second_line']}
    City       : {address['city']}
    Pincode    : {address['pincode']}
    State      : {address['state']}
    Country    : {address['country']}
    Phone      : {address['phone']}
    ------------------------------------------------------------
            """)
            x += 1
        choose_address(user_address,addressidx,x)
    else:
        enter_address()

def enter_address():
    filename = "address.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                addresses = json.load(f)
            except json.JSONDecodeError:
                addresses = []
    else:
        addresses = []

    temp_address = {"name": input("Enter name of Receiver :"),
                    "first_line": input("Enter Door number and Building name :"),
                    "second_line": input("Enter Street name and Area name :"),
                    "city": input("Enter name of the City :"), "pincode": input("Enter pincode :"),
                    "state": input("Enter name of the State :"), "country": input("Enter name of the Country :"),
                    "phone" : input("Enter Phone Number of Receiver :")}

    print(f"""
    ------------------------------------------------------------
    PLEASE CONFIRM YOUR ADDRESS
    Name       : {temp_address['name']}
    Address    : {temp_address['first_line']}
                 {temp_address['second_line']}
    City       : {temp_address['city']}
    Pincode    : {temp_address['pincode']}
    State      : {temp_address['state']}
    Country    : {temp_address['country']}
    Phone      : {temp_address['phone']}
    ------------------------------------------------------------
    """)

    print('''
    1 - Yes
    2 - Enter address again
        ''')
    while True:
        n = int(input("> "))
        if n == 1:
            break
        elif n == 2:
            return enter_address()
        else:
            print("Invalid input... Try again :(")
    user_found = False
    email = s.logged_in_user
    for address in addresses:
        if email == address["email"]:
            address["address"].append(temp_address)
            user_found = True
            break
    if not user_found:
        addresses.append({
            "email": email,
            "address": [temp_address]
        })
    with open(filename, "w") as f:
        json.dump(addresses, f, indent=4)
    return temp_address


def choose_address(user_address,addressidx,x):
    print(f'''\tEnter serial number of the address to select it
    or Enter {x} to Enter a new address
    (or 0 to go back): ''')
    ch = int(input("> "))
    if ch in addressidx:
        chosen_address = user_address[ch - 1]
        print(f"""
    ------------------------------------------------------------
    YOU CHOSE
    Name       : {chosen_address['name']}
    Address    : {chosen_address['first_line']}
                 {chosen_address['second_line']}
    City       : {chosen_address['city']}
    Pincode    : {chosen_address['pincode']}
    State      : {chosen_address['state']}
    Country    : {chosen_address['country']}
    Phone      : {chosen_address['phone']}
    ------------------------------------------------------------
                                    """)
        print('''
    1 - Yes
    2 - Choose again
                ''')
        while True:
            n = int(input("> "))
            if n == 1:
                break
            elif n == 2:
                return select_address()
            else:
                print("Invalid input... Try again :(")
        return place_order(chosen_address)
    elif ch == x:
        chosen_address = enter_address()
        place_order(chosen_address)
    elif ch == 0:
        return view_cart()
    else:
        print("Address with given serial number doesnt exist... Try again :(")
        return choose_address(user_address, addressidx, x)

def place_order(chosen_address):

    filename = "cart.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                carts = json.load(f)
            except json.JSONDecodeError:
                carts = []
    else:
        carts = []
    current_user_cart = []
    grand_total = 0
    for user_cart in carts:
        if user_cart["email"] == s.logged_in_user:
            current_user_cart = user_cart['cart']
            for prod in user_cart['cart']:
                total = prod['price'] * prod['quantity']
                grand_total += total
            break

    today = date.today()
    mdates = []
    for i in range(1, 6):
        mdates.append(today + timedelta(days=i))
    datesidx = []
    x = 1
    print("""
    Choose a delivery date
    (or Enter 0 to cancel order)
        """)
    dates =  mdates[1:]
    for d in dates:
        print(f"\t{x} - {d}")
        datesidx.append(x)
        x+=1
    delivery_date = dates[choose_date(datesidx)]
    payment_method = make_payment(grand_total)


    order_details = { "email" : s.logged_in_user, "cart" : current_user_cart,
                      "address" : chosen_address, "date_placed" : today.strftime("%Y-%m-%d"),
                      "delivery_date" : delivery_date.strftime("%Y-%m-%d"), "payment_method" : payment_method,
                      "order_total" : grand_total,"status" : "Order Placed"}

    filename = "orders.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                orders = json.load(f)
            except json.JSONDecodeError:
                orders = []
    else:
        orders = []

    email = s.logged_in_user
    user_found = False
    for order in orders:
        if email == order["email"]:
            order["order_details"].append(order_details)
            user_found = True
            break

    flag = perform_updates(order_details)
    if flag:
        if user_found:
            with open(filename, "w") as f:
                json.dump(orders, f, indent=4)

        else:
            orders.append({
                "email": email,
                "order_details": [order_details]
            })
            with open(filename, "w") as f:
                json.dump(orders, f, indent=4)
        print("Order placed successfully...  Thank you for choosing Cheeeee shop :)")
        return customer_menu()
    else:
        print("Unable to place order... Try again :(")
        return view_cart()

def make_payment(grand_total):
    payment_modes = ["CASH ON DELIVERY", "SCANNER", "UPI", "CARD"]
    print(f"***** Your Order Total is {grand_total}")
    paymentidx = []
    for i in range(0, len(payment_modes)):
        print(f"{i+1} - {payment_modes[i]}")
        paymentidx.append(i+1)
    ch = choose_payment_method(paymentidx)
    method = payment_modes[ch]
    if method == payment_modes[0]:
        return method
    elif method == payment_modes[1]:
        print("scanner here")
        time.sleep(3)
        print("Payment Completed...")
        return method
    elif method == payment_modes[2]:
        upi = input("Enter your upi id :")
        print(f"Payment request sent to {upi}")
        time.sleep(3)
        print("Payment Completed...")
        return method
    elif method == payment_modes[3]:
        name = input("Enter name on the card : ")
        card = input("Enter your card number : ")
        expiry = input("Enter your card Expiry mmyy : ")
        cvv = input("Enter your card CVV : ")
        otp = input("Enter OTP to Authorise transaction : ")
        time.sleep(3)
        print("Payment Completed...")
        return method


def choose_payment_method(paymentidx):
    m = int(input("""
    Choose a Payment Method
    (or 0 to cancel)
    > """))
    if m in paymentidx:
        return m-1
    elif m == 0:
        return view_cart()
    else:
        print("Invalid input... Try again :(")
        choose_payment_method(paymentidx)

def choose_date(datesidx):
    m = int(input("""
        > """))
    if m in datesidx:
        return m-1
    elif m == 0:
        return view_cart()
    else:
        print("Invalid input... Try again :(")
        return choose_date(datesidx)

def perform_updates(order_details):
    filename1 = "products.json"
    filename2 = "cart.json"
    with open(filename1, "r") as f:
        products = json.load(f)
    with open(filename2, "r") as f:
        carts = json.load(f)

    n = 0
    for product in products:
        for item in order_details["cart"]:
            if product["name"] == item["name"]:
                product["quantity"] -= item["quantity"]
                n += 1
    if n == len(order_details["cart"]):
        for cart in carts:
            if cart["email"] == s.logged_in_user:
                cart["cart"].clear()
        with open(filename1, "w") as f:
            json.dump(products, f, indent=4)
        with open(filename2, "w") as f:
            json.dump(carts, f, indent=4)
        return True
    else:
        return False

