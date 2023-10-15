import contacts
import notebook
import sorter
import re
import file_handler
from collections import UserDict

contacts_path = "contact_book.bin"
note_path = "notes.bin"

def main():
    phone_book = contacts.AddressBook()   

    is_running = True

    while is_running:
        user_input = input("Choose (contacts, notes, sorter): ").lower() #тут треба прописати вибір з чим саме будемо працювати. Типу до списку контактів, нотатника чи сортера
        
        if user_input == "contacts":
            phone_book = file_handler.load_data(contacts_path)
            while True:
                user_input = input("Enter command: ").lower()

                if user_input == "hello":
                    print(contacts.hello())
                elif user_input.startswith("add"):
                    _, name, phone = user_input.split()
                    print(contacts.add_contact(name, phone))          
                elif user_input.startswith("change"):
                    _, name, phone = user_input.split()
                    print(contacts.change_contact(name, phone))
                elif user_input.startswith("phone"):
                    _, name = user_input.split()
                    print(contacts.get_phone(name))
                elif user_input == "show all":
                    print(contacts.show_all())
                
                elif user_input.startswith("search"):
                    _, query = user_input.split()
                    results = contacts.phone_book.search(query)
                    if results:
                        for record in results:
                            print(f"Name: {record.name.value}, Phone: {', '.join(contacts.phone.value for phone in contacts.record.phones)}")
                    else:
                        print("No matching contacts found.")
                elif user_input.startswith("upcoming birthdays"):
                    _, days = user_input.split()
                    days = int(days)
                    upcoming_birthdays = phone_book.find_upcoming_birthdays(days)
                    if upcoming_birthdays:
                        print("Upcoming Birthdays:")
                        for record in upcoming_birthdays:
                            name = record.name.value
                            birthday = record.birthday.value.strftime("%Y-%m-%d")
                            print(f"{name} ({birthday})")
                    else:
                        print("No upcoming birthdays found.")
                elif user_input == "back":
                    file_handler.save_data(phone_book, contacts_path)
                    break
                elif user_input in ["good bye", "close", "exit"]:
                    file_handler.save_data(phone_book, contacts_path)
                    print(contacts.goodbye())
                    is_running = False
                    break
        elif user_input == "notes":
            phone_book.data = file_handler.load_data(note_path)
            pass                      #Сюди додаєм роботу з нотатником

        elif user_input == "sorter":
            pass                      #Тут прописуєм роботу з сортером. Це має бути 1 команда - вказати папку яку будем сортувати
        
        elif user_input in ["good bye", "close", "exit"]:
            print(contacts.goodbye())
            is_running = False
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()