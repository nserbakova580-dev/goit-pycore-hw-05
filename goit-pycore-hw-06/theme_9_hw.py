#попрацювати над внутрішньою логікою асистента:
#як зберігаються дані, які саме дані та 
#що з ними можна зробити - реалізувати сутності:

#   Field: Базовий клас для полів запису.
#	Name: клас для зберігання імені контакту.
#	Phone: клас для зберігання номера телефону.
#	Record: клас для зберігання інфо про контакт 
# (включно з іменем та списком телефонів).
#	AddressBook: клас для зберігання записів та керування ними


# DDD Model

# Models: phone_obj = Phone(phone) - исключения выбрасывает Phone

class Field: # value storage and interface
    def __init__(self, value: str):

        if not isinstance(value, str):
            raise TypeError("Value must be a string.")    
        self._value = self.validate(value)

    def validate(self, value: str) -> str: # перевірка в дочірних класах
        return value

    @property
    def value(self) -> str: 
        return self._value # name.value як до атрибуту
    
    def __str__(self) -> str: # формат друку 
        return self._value

    def __eq__(self, other) -> bool: # сравнение содержимого, а не адресов памяти: value-object определяется значением
        return isinstance(other, self.__class__) and self._value == other._value

    def __hash__(self): # використання value-obj як ключа в dict
        return hash(self._value)

    
class Name(Field): # value object
    
    def validate(self, value: str):
        if not value:            
            raise ValueError("Name cannot be empty.")
        return value

class Phone(Field):

    def validate(self, value: str) -> str:
        value = value.strip()

        if value.startswith("+"):
            value = value[1:]

        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")

        return value

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value!r})"

# Aggregate Root:
   
class Record: # entity for Name and Phone storage; phone numbers add/delete
    def __init__(self, name: Name):
        if not isinstance(name, Name):
            raise TypeError("Expected Name instance.")
        self.name = name
        self._phones: list[Phone] = []

    @property
    def phones(self): # захист від зовнішніх generate-функцій (.append(), ...)
        return tuple(self._phones)

    def find_phone(self, phone: str) -> Phone:
        for p in self._phones:
            if p.value == phone:
                return p
        raise ValueError ("Phone not found.")   

    def add_phone(self, phone: str) -> None:
        for p in self._phones:
            if p.value == phone:
                raise ValueError("Phone already exists.")

        self._phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        
        phone_obj = self.find_phone(old_phone)
   
        new_phone_obj = Phone(new_phone)
        index = self._phones.index(phone_obj)
        self._phones[index] = new_phone_obj


    def remove_phone(self, phone: str) -> None: 
        phone_obj = self.find_phone(phone) 
        self._phones.remove(phone_obj)

    def __str__(self):
        phones = ", ".join(p.value for p in self._phones) or "no phones"
        return f"{self.name.value}: {phones}"

 # aggregate collection/Repository - records: find, validate and storage            
                
class AddressBook:
    def __init__(self):
        self._records: dict[str, Record] = {}

    def add_record(self, record: Record):
        key = record.name.value.lower()
        if key in self._records:
            raise ValueError("Record already exists.")
        self._records[key] = record

    def find(self, name: str) -> Record:
        key = name.lower()
        if key not in self._records:
            raise KeyError("Record not found.")
        return self._records[key]

    def delete(self, name: str):
        key = name.lower()
        if key not in self._records:
            raise KeyError("Record not found.")
        del self._records[key]

    def __str__(self):
        return "\n".join(str(record) for record in self._records.values())
 
# Application Layer: commands

def input_error(func): # декоратор обробки помилок
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments."
    return inner

book = AddressBook()

@input_error
def add_record(args):
    if len(args) != 2:
        raise ValueError("Usage: add record <name> <phone>")

    name, phone = args

    try:
        book.find(name)
    except KeyError:
        record = Record(Name(name))
        record.add_phone(phone)
        book.add_record(record)
    else:
        raise ValueError("Contact already exists.")

    return "Contact added."

@input_error
def find(args):
    name = args[0]
    record = book.find(name)
    return str(record)

@input_error
def delete(args):
    name = args[0]
    book.delete(name)
    return f"Contact deleted."

@input_error
def add_phone(args):
    if len(args) != 2:
        raise ValueError("Usage: add phone <name> <phone>")

    name, phone = args
    record = book.find(name)
    record.add_phone(phone)

    return "Phone added."

@input_error
def remove_phone(args):
    if len(args) != 2:
        raise ValueError("Usage: remove-phone <name> <phone>")
    name, phone = args
    record = book.find(name)
    record.remove_phone(phone)

    return "Phone removed."

@input_error
def edit_phone(args):
    if len(args) != 3:
        raise ValueError("Usage: edit-phone <name> <old_phone> <new_phone>")

    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)

    return "Phone updated."

@input_error
def find_phone(args):
    if len(args) != 2:
        raise ValueError("Usage: find-phone <name> <phone>")

    name, phone = args
    record = book.find(name)
    phone_obj = record.find_phone(phone)

    return f"Phone found: {phone_obj.value}"


# Парсер: команда (на першому місці) + аргумент(и) (для деяких команд відсутній)

def parse_input(user_input: str):

    if not user_input.strip():
        raise ValueError("Empty input.")

    parts = user_input.strip().split()

    if parts[0].lower() in ("exit", "close"):
        return parts[0].lower(), []

    if len(parts) >= 2:
        command = " ".join(parts[:2]).lower()
        args = parts[2:]
    else:
        command = parts[0].lower()
        args = []

    return command, args

# Dispatcher 

def dispatch_command(command: str, args: list[str]) -> str:
    commands = {
        "add record": add_record,
        "find record": find,
        "delete record": delete,
        "add phone": add_phone,
        "remove phone": remove_phone,
        "edit phone": edit_phone,
        "find phone": find_phone
    }

    handler = commands.get(command)

    if handler is None:
        return "Unknown command."

    return handler(args)

# CLI (input, print) (+ pickle (load/save))

def main(): 

    print("Welcome to the assistant bot!")
    print(
"""Available commands:

Record:
  add record
  find record
  delete record

Phone:
  add phone
  remove phone
  edit phone
  find phone

System:
  exit
  close
"""
)
    while True:
        user_input = input(">>> ")

        try:
            command, args = parse_input(user_input)

            if command in ("exit", "close"):
                print("Good bye!")
                break

            result = dispatch_command(command, args)
            print(result)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()


