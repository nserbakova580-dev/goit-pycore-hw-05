#Треба: розробити Python-скрипт для аналізу файлів логів:
#скрипт повинен читати лог-файл, переданий як аргумент командного рядка,
#виводити статистику за рівнями логування (INFO, ERROR, DEBUG),
#користувач може вказати рівень логування як другий аргумент командного рядка, 
#щоб отримати всі записи цього рівня.


from datetime import datetime
from collections import defaultdict
from tabulate import tabulate
import sys
import os

# декоратор перевірки аргументів командної строки:

def validate_cli_args(func): #High-Order Function + Closure as Functional Programming
    def wrapper():

        if len(sys.argv) < 2:
            print("Usage: main.py <path_to_log<file> [LEVEL]")
            sys.exit(1)

        file_path = sys.argv[1]
        level = sys.argv[2].upper() if len(sys.argv) > 2 else None

        if not os.path.exists(file_path):
            print(f"Error: file '{file_path} doen't exist")
            sys.exit(1)

        return func(file_path, level)

    return wrapper

# повретає список словників, де кожна строка - словник:

def load_logs(file_path: str) -> list:

    logs = []

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)

    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        sys.exit(1)

    except PermissionError:
        print(f"Error: no permission to read '{file_path}'.")
        sys.exit(1)

    except OSError as e:
        print(f"I/O error while reading file: {e}")
        sys.exit(1)

    return logs

# парсінг - 4 компоненти для кожної строки (min перших 3):

def parse_log_line(line: str) -> dict | None:

    line = line.strip()

    if not line: #немає самої строки
        return None

    parts = line.split()
    if len(parts) < 3: #немає, що аналізувати
        return None

    date_str, time_str = parts[0], parts[1]

    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    except ValueError: #некоректна дата
        return None

    level = parts[2]
    if not level.isupper(): #немає ключовогоо параметру для аналізу
        return None 

    message = " ".join(parts[3:]) if len(parts) > 3 else "" #без message аналізувати Level ще можливо

    return {
        "date": dt.date(),
        "time": dt.time(),
        "level": level,
        "message": message
    }

# підрахунок кількості записів для кожоного рівня логування:

def count_logs_by_level(logs: list) -> dict:

    counts = defaultdict(int) #

    for log in logs:
        level = log.get("level")
        if level:
            counts[level] += 1

    return dict(counts)

# список записів для конкретного рівня логування     

def filter_logs_by_level(logs: list, level: str) -> list: 

    level = level.upper()

    return [log for log in logs if log.get("level") == level] #List Comprehension as Functional Programminng

# таблиця зі статистикою даних, що були запитані клієнтом:

def display_log_counts(counts: dict) -> None:

    table = [(level, count) for level, count in sorted(counts.items())]
    headers = ["Рівень логування", "Кількість"]

    print(tabulate(table, headers, tablefmt="github")) 

# отримання CLI-аргументів - підтримує 2 варіанти запуску:
# python main.py logfile.log python АБО main.py logfile.log LEVEL:

@validate_cli_args 
def main(file_path: str, level: str | None):
    
    logs = load_logs(file_path)

    counts = count_logs_by_level(logs) #кількість записів по рівнях логування

    display_log_counts(counts) 
  
    if level:
        filtered_logs = filter_logs_by_level(logs, level)
        print(f"\nДеталі логів для рівня '{level}':\n")

        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")

if __name__ == "__main__":
    main()


