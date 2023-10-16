from collections import UserDict
from datetime import datetime
import re
import pickle

class Field:
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone_number):
        if not self.validate_phone_number(phone_number):
            raise ValueError("Invalid phone number format")
        super().__init__(phone_number)

    @staticmethod
    def validate_phone_number(phone_number):
        pattern = r'^\d{10,}$'
        return True if re.match(pattern, phone_number) else False

    @Field.value.setter
    def value(self, new_phone_number):
        if not self.validate_phone_number(new_phone_number):
            raise ValueError("Invalid phone number format")
        self._value = new_phone_number

class Email(Field):
    def __init__(self, contact_email):
        if not self.validate_contact_email(contact_email):
            raise ValueError("Invalid email format")
        super().__init__(contact_email)

    @staticmethod
    def validate_contact_email(contact_email):
        email_pattern = r"[A-Za-z]+[\.?\w+]+@\w+\.\w{2,}"
        return len(re.findall(email_pattern, contact_email)) > 0
    
    @Field.value.setter
    def value(self, new_contact_email):
        if not self.validate_contact_email(new_contact_email):
            raise ValueError("Invalid email format")
        self._value = new_contact_email

class Address(Field):
    def __init__(self, contact_address):
        super().__init__(contact_address)

class Record:
    def __init__(self, phone, email=None, address=None, birthday=None):
        #self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = ''
        self.add_phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def add_email(self, contact_email):
        email = Email(contact_email)
        self.emails.append(email)

    def edit_email(self, old_contact_email, new_contact_email):
        if not Email.validate_contact_email(new_contact_email):
            raise ValueError("Invalid email format")    
        found = False
        for email in self.emails:
            if email.value == old_contact_email:
                email.value = new_contact_email
                found = True
        if not found:
            raise ValueError("Such email not found in the record")

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        if not Phone.validate_phone_number(new_phone_number):
            raise ValueError("Invalid phone number format")
        
        found = False
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                found = True
        
        if not found:
            raise ValueError("Phone number not found in the record")
            

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def set_address(self, address):
        self.address = address

    def set_email(self, email):
        self.email.append(email)

    def set_birthday(self, birthday):
        self.birthday = birthday
    
    def days_to_birthday(self):
        if not self.birthday:
            return None                   
        birthday = self.birthday
        today = datetime.today()
        year, month, day = map(int, birthday.split('-'))
        next_birthday = datetime(today.year, month, day)

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, month, day)

        delta = next_birthday - today
        days_until_birthday = delta.days
        
        return f"There are {days_until_birthday} days to next birthday."

class Birthday(Field):
    def __init__(self, birthday):
        if not self.validate_birthday(birthday):
            raise ValueError("Invalid birthday format")
        super().__init__(birthday)

    @staticmethod
    def validate_birthday(birthday):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return True if re.match(pattern, birthday) else False
    
    @Field.value.setter
    def value(self, new_birthday):
        if not self.validate_birthday(new_birthday):
            raise ValueError("Invalid birthday format")
        self._value = new_birthday

class AddressBook(UserDict):
    def __init__(self, file_path = "contact_book.bin"):
        self.data = {}
        self.file_path = file_path
        self.load_data()
        self.page_size = 10  

    def iterator(self):
        page = 0  
        while page * self.page_size < len(self.data):
            start = page * self.page_size
            end = (page + 1) * self.page_size
            yield list(self.data.values())[start:end]
            page += 1

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def add_birthday(self, name, birthday):
        if not Birthday.validate_birthday(birthday):
            raise ValueError("Invalid birthday format")
        if name in self.data:
            self.data[name].set_birthday(birthday)
            print(f"Birthday added for {name.title()}.")
            
        else:
            print(f"Contact {name.title()} not found.")
        
    def add_email(self, name, email):
        if not Email.validate_contact_email(email):
            raise ValueError("Invalid email format")
        elif name in self.data:
            self.data[name].set_email(email)
            print(f"Email added for {name.title()}.")
        else:
            print(f"Contact {name.title()} not found.")

    def add_address(self, name, address):
        if name in self.data:
            self.data[name].set_address(address)
            print(f"Address added for {name.title()}.")
        else:
            print(f"Contact {name.title()} not found.")
    
    def edit_birthday(self, name, new_birthday):
        if not Birthday.validate_birthday(new_birthday):
            raise ValueError("Invalid birthday format")
        self.data[name].set_birthday(new_birthday)


    def load_data(self):
        try:
            with open(self.file_path, 'rb') as file:
                data = pickle.load(file)
            self.data = data
        except (FileNotFoundError, EOFError):
            print(f"Loaded data from {self.file_path}")

    def save_data(self):
        
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.data, file)
            print(f"Saved data to {self.file_path}")

    def __del__(self):
        self.save_data() 

    def search(self, query):
        search_match = []
        for name, record in self.data.items():
            if query in name or any(query in phone.value for phone in record.phones):
                search_match.append(record)
        return search_match

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name.title()} has been deleted."
        else:
            return f"Contact {name.title()} not found."

    def find_upcoming_birthdays(self, days):
        current_datetime = datetime.now()
        today = current_datetime.date()
        upcoming_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                year, month, day = record.birthday.split("-")
                birthday_date = datetime(year=today.year, month=int(month), day=int(day)).date()
                days_until_birthday = (birthday_date - today).days
                if 0 < days_until_birthday <= days:
                    upcoming_birthdays.append((name, days_until_birthday))
        
        #upcoming_birthdays.sort(key=lambda x: x[1])  
        return upcoming_birthdays

    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyError:
                return "Enter user name"
            except ValueError:
                return "Give me name and phone please"
            except IndexError:
                return "Invalid command"

        return inner

    
    def hello(self):
        return "How can I help you?"

    @input_error
    def add_contact(self, name, phone):
        if not Phone.validate_phone_number(phone):
            return "Invalid phone number format"

        self.data[name] = Record(phone)
        return f"Added {name.title()} with phone {phone}"

    @input_error
    def change_contact(self, name, phone):
        if name in data:
            self.data[name] = phone
            return f"Changed phone for {name.title()} to {phone}"
        else:
            return f"Contact {name.title()} not found"

    @input_error
    def get_phone(self, name):
        if name in self.data:
            return f"The phone for {name.title()} is {data[name]}"
        else:
            return f"Contact {name.title()} not found"
    def __str__(self):
        return self.data
    @input_error
    def show_all(self):
        
        if not self.data:
            return "Phone book is empty"
        else:
            for name, record in self.data.items():
                for phone in record.phones:
                    print(f"{name.title()}: tel.: {phone._value}, B: {record.birthday}")
           

    @input_error
    def goodbye(self):
        return "Good bye!"