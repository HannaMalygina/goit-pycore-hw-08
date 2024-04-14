from collections import UserDict
from datetime import datetime, timedelta
import pickle
import copy

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        self.set_phone(value)
        
    def validate_phone(phone_str):
        if len(phone_str) != 10 or not phone_str.isdigit():
            raise ValueError(f'Invalid phone number {phone_str}. Must contain 10 digits')

    def set_phone(self, phone_str):
        Phone.validate_phone(phone_str)
        super().__init__(phone_str)

class Birthday(Field):
    def __init__(self, value):
        self.value = None
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday: self.add_birthday(birthday)
    
    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def add_phone(self, phone_str):
        Phone.validate_phone(phone_str)
        self.phones.append(Phone(phone_str))           

    def edit_phone(self, phone_str, new_phone_str):
        self.find_phone(phone_str).set_phone(new_phone_str)

    def remove_phone(self, phone_str):
        self.phones.remove(self.find_phone(phone_str))
            
    def find_phone(self, phone_str):
        for phone_obj in self.phones:
            if phone_str == phone_obj.value:
                return phone_obj
        raise ValueError(f"Phone number {phone_str} not found")
    
    def print_phones(self):
        return f"{'; '.join(p.value for p in self.phones)}"


    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday: result += f", birthday: {self.birthday}"
        return result

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record 

    def find(self, name_str):
        return self.data.get(name_str)
        #return self.data[name_str]

    def delete(self, name_str):
        del self.data[name_str]

    def get_upcoming_birthdays(self):
        congratulation_list = []
        today = datetime.today().date()
        for _,user in self.data.items():
            #birthdate = datetime.strptime(user.birthday, "%Y.%m.%d").date()
            birthdate = user.birthday.value
            birthdate_this_year = birthdate.replace(year = today.year)
            congratulation_date = today

            #if birthday already, passed go to the next year 
            if (birthdate_this_year < today-timedelta(days=2)): 
                congratulation_date = birthdate.replace(year = today.year+1)
            #if birthday was last weekend and today is monday
            elif (birthdate_this_year == today-timedelta(days=2) or (birthdate_this_year == today-timedelta(days=1))) and today.weekday() == 0:
                congratulation_date = today
            else:
                if (birthdate_this_year.weekday()==5):
                    congratulation_date = birthdate_this_year + timedelta(days=2)
                elif (birthdate_this_year.weekday()==6):
                    congratulation_date = birthdate_this_year + timedelta(days=1)
                else:
                    congratulation_date = birthdate_this_year
            if (today + timedelta(days=7) > congratulation_date):
                congratulation_list.append({"name": user.name.value, "congratulation_date" : congratulation_date.strftime("%Y.%m.%d")})

        return congratulation_list
    
    #def __getstate__(self):
    #    return super().__getstate__()

if __name__ == "__main__":
    # record = Record("john")
    # record.add_phone("0123456789")
    # print(record)
    # record.add_phone("1234567809")
    # print(record)
    # record.edit_phone("1234567809", "12")
    # record.remove_phone("1234567809")
            

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("09.04.2001")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("07.04.2001")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(*[record for record in book.data.values()])

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223833")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
    print(book.get_upcoming_birthdays())
    # Видалення запису Jane
    book.delete("Jane")
