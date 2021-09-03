import random


def show_menu():
    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        mode = input()
        if mode in "012":
            return mode

IIN = "400000"
cards = {}

def create_account():
    while True:
        account = random.randint(0, 999999999)
        if account not in cards:
            break

    checksum = random.randint(0, 9)
    pin = random.randint(0, 9999)
    cards[account] = [checksum, pin, 0]
    print("Your card has been created")
    print("Your card number:")
    print("{0}{1:09d}{2}".format(IIN, account, checksum))
    print("Your card PIN:")
    print("{0:04d}".format(pin))
    return

def login():
    print("Enter your card number:")
    card_number = input()
    print("Enter your PIN:")
    pin = int(input())
    if len(card_number) == 16:
        card_iin = card_number[:6]
        account = int(card_number[6:15])
        card_crc = int(card_number[15])
        if card_iin == IIN and account in cards:
            account_data = cards[account]
            if account_data[1] == pin and account_data[0] == card_crc:
                print("You have successfully logged in!")
                return True
    print("Wrong card number or PIN!")
    return False

def login_menu():
    while True:
        print("1. Balance")
        print("2. Log out")
        print("0. Exit")
        mode = input()
        if mode in "012":
            return mode

while True:
    mode = show_menu()
    if mode == "1":
        create_account()
    elif mode == "2":
        log_in = login()
        if log_in:
            login_mode = login_menu()
            if login_mode == "0":
                mode = "0"
            elif login_mode == "2":
                pass
            else:
                print("Balance: 0")

    if mode == "0":
        break


