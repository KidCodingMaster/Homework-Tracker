import shelve
import random
import string


class Teacher:
    def __init__(self, name):
        self.name = name

    def run(self):
        print("You are logged in as a teacher")


def generate_password():
    characters = list(string.punctuation + string.ascii_letters + string.digits)
    random.shuffle(characters)

    password = "".join(characters[:10])

    with shelve.open("usernames.db") as db:
        if password in db.values():
            return generate_password()

    return password


def signup(username, person_type):
    password = generate_password()

    with shelve.open("usernames.db") as db:
        if username in db:
            print("You already have an account!")
            return

        db[username] = password

    print(f"Your password is {password}")

    print("Signup Successful!")

    if person_type == "teacher":
        person = Teacher(username)

        person.run()


def login(username, password, person_type):
    with shelve.open("usernames.db") as db:
        if username in db:
            if db[username] == password:
                print("Login Successful!")

                if person_type == "teacher":
                    person = Teacher(username)

                    person.run()
            else:
                print("Incorrect password!")
        else:
            print("Username not found!")


person = input("Are you a teacher or a student? ")

login_type = input("Do you want to login or signup? ").lower()

if login_type == "signup":
    username = input("What is your name? ")

    signup(username, person)
elif login_type == "login":
    username = input("Your name: ")
    password = input("Password: ")

    login(username, password, person)
