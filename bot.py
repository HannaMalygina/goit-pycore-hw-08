from AddressBook import *

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return print(e)
        except IndexError as e:
            return print("One more parameter required")
        except KeyError as e:
            return print("Name not found in contacts")
    return inner



def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name = args[0]
    phone = args[1]
    record = contacts.find(name)
    message = "Contact updated"
    if record is None:
        record = Record(name)
        contacts.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change(args, contacts):
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]
    record = contacts.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone changed."
    #else:
        #record.add_phone(new_phone)
        #return f"Phone {old_phone} was not found for {name}. I added a new phone {new_phone}."
        

@input_error
def phone(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record: return record.print_phones()
    else:
        #return add_contact(args, contacts)
        return f"{name} is not in contacts. At first create a contact using 'add' command"

@input_error
def add_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record:
        record.add_birthday(args[1])
        return f"Birthday {args[1]} added for {name}"
    else:
        #return add_contact(args, contacts)
        return f"{name} is not in contacts. At first create a contact using 'add' command"

@input_error
def show_birthday(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record: 
        if record.birthday: return record.birthday
        else: return f"{name} does not have birthday saved"
    else:
        #return add_contact(args, contacts)
        return f"{name} is not in contacts. At first create a contact using 'add' command"
    
    

#def birthdays(contacts):
    #contacts.get_upcoming_birthdays()

def all(contacts):
    res_str = ""
    for key, item in contacts.items(): res_str += f"{key} : {item} \n"
    return res_str[:-2:] 

def save_data(book, filename = "addressbook.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(book, file)

def load_data(filename = "addressbook.pkl"):
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return AddressBook()


def main():
    contacts = load_data()
    #contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change(args, contacts))
        elif command == "phone":
            print(phone(args, contacts))
        elif command == "all":
            print(all(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(contacts.get_upcoming_birthdays())
        else:
            print("Invalid command.")

    save_data(contacts)

if __name__ == "__main__":
    main()
