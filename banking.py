# Write your code here
import random
import sqlite3


class Account:
    def __init__(self, card_number, pin_code):
        self.card_number = card_number
        self.pin_code = pin_code
        self.amount = cur.execute(f"SELECT balance FROM card WHERE number = {self.card_number}").fetchone()[0]


def get_balance(acc):
    return cur.execute(f"SELECT balance FROM card WHERE number = {acc}").fetchone()[0]


def add_account():
    random.seed()
    generated_card_number = card_number_generation()
    while generated_card_number in cur.execute("SELECT number FROM card").fetchall():
        generated_card_number = card_number_generation()
    generated_pin_code = "".join(str(random.randint(0, 9)) for _ in range(4))
    cur.execute(f"INSERT INTO card (number, pin) VALUES ({generated_card_number}, {generated_pin_code})")
    conn.commit()
    return Account(generated_card_number, generated_pin_code)


def card_number_generation():
    random.seed()
    generated_card_number = "400000" + "".join(str(random.randint(0, 9)) for _ in range(9))
    generated_card_number = generated_card_number + checksum_generation(generated_card_number)
    return generated_card_number


def checksum_generation(card_num):
    card_num_list = list(map(int, card_num))
    card_num_list[0::2] = [x * 2 for x in card_num_list[0::2]]
    card_num_list = [x - 9 if x >= 10 else x for x in card_num_list]
    checksum = (10 - sum(card_num_list) % 10) % 10
    return str(checksum)


def table_check():
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='card'")
    if cur.fetchone()[0] == 0:
        cur.execute("CREATE TABLE card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
        conn.commit()


def cred_check(num, pin):
    if_card_exists = cur.execute(f"SELECT count(*) FROM card WHERE number = {num} and pin = {pin}").fetchone()[0]
    return True if if_card_exists == 1 else False


def add_income(income):
    cur.execute(f'UPDATE card SET balance = {get_balance(account.card_number) + income} WHERE number = {account.card_number}')
    conn.commit()


def do_transfer(dest):
    if dest[-1] == checksum_generation(dest[0:15]):
        if dest in [i[0] for i in cur.execute(f"SELECT number FROM card").fetchall()]:
            transfer_amount = int(input("Enter how much money you want to transfer:\n"))
            if get_balance(account.card_number) >= transfer_amount:
                cur.execute(f"UPDATE card SET balance = {get_balance(account.card_number) - transfer_amount} WHERE number = {account.card_number}")
                cur.execute(f"UPDATE card SET balance = {get_balance(dest) + transfer_amount} WHERE number = {dest}")
                conn.commit()
                print("Success!")
            else:
                print("Not enough money!")
        else:
            print("Such a card does not exist.")
    else:
        print("Probably you made a mistake in the card number. Please try again!")


def close_account(number):
    cur.execute(f"DELETE FROM card WHERE number = {number}")
    conn.commit()
    print("The account has been closed!")


conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
table_check()


while True:
    print("1. Create an account\n2. Log into account\n0. Exit")
    user_input = input()
    if user_input == "1":
        account = add_account()
        print(f"Your card has been created\nYour card number:\n{account.card_number}\n Your card PIN:\n{account.pin_code}")
    elif user_input == "2":
        user_card_number = int(input("Enter your card number:\n"))
        user_pin_code = int(input("Enter your PIN:\n"))
        if cred_check(user_card_number, user_pin_code):
            print("You have successfully logged in!")
            account = Account(user_card_number, user_pin_code)
            while True:
                print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
                user_input = input()
                if user_input == "1":
                    print(f"Balance: {get_balance(account.card_number)}")
                elif user_input == "2":
                    income_amount = int(input("Enter income:\n"))
                    add_income(income_amount)
                    print("Income was added!")
                elif user_input == "3":
                    print("Transfer")
                    destination = input("Enter card number:\n")
                    do_transfer(destination)
                elif user_input == "4":
                    close_account(account.card_number)
                    break
                elif user_input == "5":
                    print("You have successfully logged out!")
                    break
                elif user_input == "0":
                    print("Bye!")
                    exit()
        else:
            print("Wrong card number or PIN")
    elif user_input == "0":
        print("Bye!")
        exit()
