import shelve
import random
import string
import json


def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)


class Teacher:
    def __init__(self, name):
        self.name = name

    def run(self):
        print("You are logged in as a teacher")

        while True:
            print("1. Add task")
            print("2. View Tasks")
            print("3. View progress")
            print("4. Logout")

            cmd = input("\nWhat do you want to do? ")

            if cmd == "1":
                name = input("What is the task? ")

                with shelve.open(settings["studentsFile"]) as db:
                    for kid in db.keys():
                        student_data = db[kid]
                        student_data["tasks"].append(name)
                        db[kid] = student_data
                        print(db[kid]["tasks"])

                print("Task added successfully!")
            elif cmd == "4":
                print("Good Bye!")

                return


class Student:
    def __init__(self, name):
        self.name = name

    def run(self):
        print("You are logged in as a student")

        while True:
            print("1. View tasks")
            print("2. Logout")

            cmd = input("What do you want to do? ")

            if cmd == "1":
                print("Tasks: ")

                with shelve.open(settings["studentsFile"]) as db:
                    tasks = db[self.name]["tasks"]

                for num, i in enumerate(tasks):
                    print(f"{num + 1}. {i}")

                print()
            elif cmd == "2":
                print("Good Bye!")

                return


def generate_password():
    characters = list(string.punctuation + string.ascii_letters + string.digits)
    random.shuffle(characters)

    password = "".join(characters[:10])

    with shelve.open(settings["usernameFile"]) as db:
        if password in db.values():
            return generate_password()

    return password


def signup(username, person_type):
    password = generate_password()

    with shelve.open(settings["usernameFile"]) as db:
        if username in db and db[username]["type"] == person_type:
            print("You already have an account!")
            return

        db[username] = {"password": password, "type": person_type}

    print(f"Your password is {password}")

    print("Signup Successful!")

    if person_type == "teacher":
        person = Teacher(username)
    elif person_type == "student":
        person = Student(username)

        with shelve.open(settings["studentsFile"]) as db:
            db[username] = {"tasks": []}

    person.run()


def login(username, password, person_type):
    with shelve.open(settings["usernameFile"]) as db:
        if username in db:
            if (
                db[username]["password"] == password
                and db[username]["type"] == person_type
            ):
                print("Login Successful!")

                if person_type == "teacher":
                    person = Teacher(username)
                elif person_type == "student":
                    person = Student(username)

                person.run()
            elif db[username]["password"] != password:
                print("Incorrect password!")
            elif db[username]["type"] != password:
                print("Incorrect type!")
        else:
            print("Username not found!")


settings = load_settings()

person = input("Are you a teacher or a student? ").lower()

if person not in ("teacher", "student"):
    print("Invalid! You can only login or signup as a teacher or a student!")

login_type = input("Do you want to login or signup? ").lower()

if login_type == "signup":
    username = input("What is your name? ")

    signup(username, person)
elif login_type == "login":
    username = input("Your name: ")
    password = input("Password: ")

    login(username, password, person)
