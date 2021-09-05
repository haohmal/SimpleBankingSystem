import random
import sqlite3

sql_create_table_accounts = """CREATE TABLE IF NOT EXISTS card (
                                id INTEGER PRIMARY KEY,
                                number TEXT,
                                pin TEXT,
                                balance INTEGER DEFAULT 0
                            );
                            """

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()

cur.execute(sql_create_table_accounts)

def select_account(conn, number):
    """
        Query card by account
        :param conn: the Connection object
        :param account:
        :return:
        """
    cur = conn.cursor()
    cur.execute("SELECT * FROM card WHERE number=?", (number,))

    row = cur.fetchone()

    print(row)
    return row

def insert_card(conn, number, pin):
    """
        insert new card
        :param conn: the Connection object
        :param account:
        :param crc:
        :param pin:
        :return:
        """
    cur = conn.cursor()
    cur.execute("INSERT INTO card (number, pin, balance) VALUES(?, ?, ?)", (number, pin, 0))

    conn.commit()
    result = cur.lastrowid
    print(result)
    return result


def get_luhn_crc(card_number):
    luhn_sum = 0
    for i in range(len(card_number)):
        n = int(card_number[i])
        if i % 2 == 0:
            n = n * 2
            if n > 9:
                n -= 9
        luhn_sum += n
    crc = luhn_sum % 10
    if crc > 0:
        crc = 10 - crc
    return crc


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
        if not select_account(conn, account):
            break

    #checksum = random.randint(0, 9)
    checksum = get_luhn_crc(IIN + "{0:09d}".format(account))
    pin = random.randint(0, 9999)
    number = "{0}{1:09d}{2}".format(IIN, account, checksum)
    #cards[account] = [checksum, pin, 0]
    _ = insert_card(conn, number, pin)
    print("Your card has been created")
    print("Your card number:")
    print(number)
    print("Your card PIN:")
    print("{0:04d}".format(pin))
    return

def login():
    print("Enter your card number:")
    card_number = input()
    print("Enter your PIN:")
    pin = input()
    #if len(card_number) == 16:
    #    card_iin = card_number[:6]
    #    account = int(card_number[6:15])
    #    card_crc = int(card_number[15])
    #    if card_iin == IIN and account in cards:
    #        account_data = cards[account]
    #        if account_data[1] == pin and account_data[0] == card_crc:
    result = select_account(conn, card_number)
    if result and result[2] == pin:
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


