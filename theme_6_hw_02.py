#є текстовий файл з інфо про котів. Кожен рядок файлу:
#унікальний ID кота, його ім'я та вік, #розділені комою.
#Треба:розробити функцію get_cats_info(path):
#читає цей файл та повертає список словників
#з інфо про кожного кота


def get_cats_info(path: str) -> list[dict]:

    try:
        with open(path, 'r', encoding = "utf-8") as file: #безпечне читання + кодування
            return list(parse_cats(file)) #утворення словнику

    #опрацьовування винятків читання файлу        
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at path: {path}")
    except OSError as error:
        raise OSError(f"I/O error: {error}")

def parse_cats(file):

    for line_number, line in enumerate(file, start=1):
        line = line.strip()

        if not line:
            continue

        parts = line.split(",") #для кожного рядка split()

        if len(parts) != 3:
            raise ValueError(f"Line {line_number}: {line} - expected 3 fields")

        cat_id_str, name, age_str = parts

        if not cat_id_str:
            raise ValueError(f"Line {line-number}: empty id")

        if not name:
            raise ValueError(f"Line {line_number}: empty name")

        try:
            age = int(age_str)
        except ValueError(f"Line {line_number}: age must be integer")

        if age <0:
             raise ValueError(f"Line {line_number}: age cannot be negative")

        yield {"id": cat_id_str, "name": name, "age": age}
