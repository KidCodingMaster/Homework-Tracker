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
            elif cmd == "2":
                with shelve.open(settings["studentsFile"]) as db:
                    tasks = db[list(db.keys())[0]]["tasks"]

                if tasks:
                    print("Tasks: ")

                    for num, i in enumerate(tasks):
                        print(f"{num + 1}. {i}")
                else:
                    print("No tasks added!")

                print()
            elif cmd == "3":
                name = input("Who's name do you want to check progress of? ")

                with shelve.open(settings["studentsFile"]) as db:
                    if name not in db.keys():
                        print("Name not found!")
                        continue

                    with shelve.open(settings["studentsFile"]) as db:
                        completed = db[list(db.keys())[0]]["completed"]
                        tasks = db[list(db.keys())[0]]["tasks"]

                    if completed:
                        print("Completed Tasks: ")

                        for num, i in enumerate(completed):
                            print(f"{num + 1}. {i}")
                    else:
                        print("No tasks completed!")

                    print()

                    incomplete = set(completed).difference(set(tasks))

                    if incomplete == set():
                        print("No Incomplete Tasks!")
                    else:
                        print("Incomplete Tasks: ")

                        for num, i in enumerate(incomplete):
                            print(f"{num + 1}. {i}")

                        print()
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
            print("2. Complete Task")
            print("3. Logout")

            cmd = input("What do you want to do? ")

            if cmd == "1":
                with shelve.open(settings["studentsFile"]) as db:
                    tasks = db[self.name]["tasks"]

                if tasks:
                    print("Tasks: ")

                    for num, i in enumerate(tasks):
                        print(f"{num + 1}. {i}")
                else:
                    print("No tasks added!")

                print()
            elif cmd == "4":
                print("Tasks: ")

                with shelve.open(settings["studentsFile"]) as db:
                    tasks = db[self.name]["tasks"]

                for num, i in enumerate(tasks):
                    print(f"{num + 1}. {i}")

                print()

                task = input("Which task do you want to complete? ")

                if not task.isdigit():
                    print("Please enter a numerical value!")
                    continue

                task_idx = int(task)

                if task > len(tasks) or task < 1:
                    print("Please enter a valid input!")
                    continue

                with shelve.open(settings["studentsFile"]) as db:
                    completed = db[self.name]["completed"]
                    completed.append(tasks[task_idx - 1])
                    db[self.name]["completed"] = completed

                    print("Task is completed!")
            elif cmd == "3":
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
            if len(db.keys()) > 0:
                db[username] = {
                    "tasks": db[list(db.keys())[0]]["tasks"],
                    "completed": [],
                }
            else:
                db[username] = {"tasks": [], "completed": []}

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
            elif db[username]["type"] != person_type:
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
