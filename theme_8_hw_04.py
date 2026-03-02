#Треба: доробити консольного бота-помічника:
#додати обробку помилок за допомогою декораторів


# Декоратор для обробки помилок :

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found. Please check the name or change the command."
        except ValueError as ve:
            return str(ve)
        except IndexError:
            return "Not enough arguments. Please provide name and/or phone."
        except Exception as e:
            return f"Unexpected error: {e}"
    return inner

# Handler-функции з обготкою: 

@input_error
def add_contact(args, contacts):
    
    if len(args) < 2: #перевірка наявності аргументів
        raise IndexError
    name, phone = args

    if name in contacts: #перевірка наявності контакта - немає потреби добавляти в контакти
        raise ValueError(f"{name} already exists")

    if not phone.isdigit(): #перевірка цифрового формату телефону - строка має тільки цифри
        raise ValueError("Phone must contain only digits")

    contacts[name] = phone

    return f"Contact {name}: {phone} added"

@input_error
def change_contact(args, contacts):
    
    if len(args) < 2:  #перевірка наявності аргументів
        raise IndexError
    name, phone = args

    if name not in contacts: #перевірка наявності контакта в словнику
        raise KeyError

    if not phone.isdigit(): #перевірка цифрового формату телефону
        raise ValueError("Phone must contain only digits")
    contacts[name] = phone

    return f"Contact {name} updated"

@input_error
def show_phone(args, contacts):
   
    if len(args) < 1: #перевірка наявності аргументів
        raise IndexError
    name = args[0]

    if name not in contacts: # перевірка наявності контакта в словнику
        raise KeyError

    return f"{name}: {contacts[name]}"

@input_error
def show_all(args, contacts):
    
    if args: #перевірка выдсутності аргументів у функції
        raise ValueError("The 'all' command does not accept arguments")

    if not contacts: #перевірка наявності контактів у словнику
        return "No contacts saved"

    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

# Парсер: команда (на першому місці) + аргумент(и) (для деяких команд відсутній)

def parse_input(user_input: str): #без декоратора
    
    if not user_input.strip(): #перевірка на наявність команди
        raise ValueError("Empty input. Please enter a command.")

    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]

    return command, args

# CLI / Dispatcher 
def main():
    contacts = {} 
    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all
    }

    print("Welcome to the assistant bot!")
    print("Available commands: add, change, phone, all, hello, close/exit")

    while True:
        user_input = input("Enter a command: ").strip()
    
        if not user_input: # Ігнорування порожнього введення
            continue

        try:
            command, args = parse_input(user_input)
        except ValueError as ve: # структурна помилка як то невірні символи 
            print(ve)
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
            continue

        handler = commands.get(command) # Перовірка на наявність команди
        if handler:
            try:
                # якщо не було введено необхідних аргументів
                if not args and command in ["add", "change", "phone"]:
                    arg_input = input("Enter arguments for the command: ").strip()
                    args = arg_input.split()
               
                print(handler(args, contacts))
            except Exception as e: # рандомні помилки
                print(f"Error: {e}")
        else:
            # якщо команду було введено невірно
            print(f"Invalid command '{command}'. Available commands: {', '.join(commands.keys())}, hello, close/exit")

if __name__ == "__main__":
    main()