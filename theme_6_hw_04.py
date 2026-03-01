#Напишіть консольного бота помічника:
#зберігає ім'я та номер телефону,
#знаходитm номер телефону за ім'ям,
#змінювє записаний номер телефону, 
#виводитm в консоль всі записи, які зберіг.


#Parser-функціональність: команда та аргументи 

def parse_input(user_input: str):

    if not user_input.strip():
        raise ValueError("empty input")

    command, *args = user_input.strip().split()
    cmd = command.lower()

    return cmd, args

# Handler-функції

def add_contact(args, contacts: dict):

    if len(args) != 2:
        raise ValueError("Usage: add <name> <phone>")

    name, phone = args

    if name in contacts:
        raise ValueError(f"Contact {name} already exists in the contacts")

    contacts[name] = phone

    return f"Contact {name}: {phone} added"

def change_contact(args, contacts:dict):   

    if len(args) != 2:
        raise ValueError("Usage: change <name> <phone>")

    name, phone = args   
    
    if name not in contacts:
        raise ValueError(f"Contact {name} not found")  

    contacts[name] = phone

    return "Contact updated"

def show_phone(args, contacts: dict):

    if len(args) != 1:
        raise ValueError("Usage: phone <name>") 

    name = args[0]

    if name not in contacts:
        raise ValueError(f"Contact {name} not found")
    
    return contacts[name]

def show_all(args, contacts: dict):

    if args:
        raise ValueError("Usage: all")

    if not contacts:
        return "No contacts saved"

    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

#CLI/Dispatcher

def main() -> None:

    contacts = {} 
    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all
    }   
    print("Welcome to the assistant bot!")

    while True:

        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]: #команда без handler
            print("Good bye!")
            break

        elif command == "hello": #hкоманда без handler
            print("How can I help you?")
            continue

        handler = commands.get(command)

        if handler: 
            result = handler(args, contacts)
            print(result)
        else:
            print("Invalid command")
    
if __name__ == "__main__":
    main()
    
      