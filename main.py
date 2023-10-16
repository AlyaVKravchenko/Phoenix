import contacts
import notebook
import sorter
import re
#import file_handler
from collections import UserDict

def main():
    phone_book = contacts.AddressBook()   

    is_running = True

    while is_running:
        user_input = input("Hello! I am your personal assistant! How can I help you? Choose one option (contacts, notes, sorter): ").lower() 
        
        if user_input == "contacts":
            print(f"Your data will be saved to {phone_book.file_path} file")
                         
            while True:
                
                user_input = input("Enter command: ").lower()

                if user_input == "hello":
                    print(phone_book.hello())

                elif user_input.startswith("new"):
                    name = input("Enter contact name: ").lower()
                    phone = input("Enter phone number: ")
                    print(phone_book.add_contact(name, phone)) 
                    phone_book.save_data()  

                elif user_input.startswith("change phone"):
                    name = input("Enter contact name: ").lower()
                    phone = input("Enter new phone number: ")
                    print(phone_book.change_contact(name, phone))
                    phone_book.save_data()

                elif user_input.startswith("delete contact"):
                    name = input("Enter contact name wich you want to delete: ").lower()
                    print(phone_book.delete_contact(name))
                    phone_book.save_data()

                elif user_input.startswith("find phone"):
                    name = input("Enter contact name: ").lower()
                    print(phone_book.get_phone(name))

                elif user_input == "show all":
                    print(phone_book.show_all())
 
                elif user_input.startswith("search"):
                    query = input("Enter part of contact name: ").lower()
                    phone_book.search(query)

                elif user_input.startswith("add_address"):
                    name = input("Enter name: ").lower()
                    address = input("Enter contact address: ")
                    phone_book.add_address(name, address)
                    phone_book.save_data()

                elif user_input.startswith("add_email"):
                    name = input("Enter name: ").lower()
                    email = input("Enter contact email: ")
                    phone_book.add_email(name, email)
                    phone_book.save_data()

                elif user_input.startswith("add_birthday"):
                    name = input("Enter name: ").lower()
                    birthday = input("Enter birthday in format 'YYYY-MM-DD': ")
                    phone_book.add_birthday(name, birthday)
                    phone_book.save_data()

                elif user_input.startswith("edit birthday"):
                    name = input("Enter name: ").lower()
                    new_birthday = input("Enter new birthday in format 'YYYY-MM-DD': ")
                    phone_book.edit_birthday(name, new_birthday)
                    phone_book.save_data()

                elif user_input == "upcoming_birthdays":
                    days = int(input("Enter the number of upcoming days: "))
                    upcoming_birthdays = phone_book.find_upcoming_birthdays(days)
                    if upcoming_birthdays:
                        print("Upcoming Birthdays:")
                        for name, days_until_birthday in upcoming_birthdays:
                            print(f"{name} ({days_until_birthday} days until their birthday)")
                    else:
                        print("No upcoming birthdays found.")

                elif user_input == "back":
                    phone_book.save_data()
                    break
                elif user_input in ["good bye", "close", "exit"]:
                    
                    print(phone_book.goodbye())
                    is_running = False
                    break
                else:
                    print("Invalid command")
        elif user_input == "notes":
            #phone_book.data = file_handler.load_data(note_path)
            pass                      #Сюди додаєм роботу з нотатником

        elif user_input == "sorter":
            pass                      #Тут прописуєм роботу з сортером. Це має бути 1 команда - вказати папку яку будем сортувати
        
        elif user_input in ["good bye", "close", "exit"]:
            print(phone_book.goodbye())
            is_running = False
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()