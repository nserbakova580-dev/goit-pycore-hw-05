#Є текстовий файл з інфо про місячні з/п розробників:
#кожен рядок у файлі містить прізвище розробника та 
#його з/п, які розділені комою без пробілів. 
#Треба: розробити функцію total_salary(path), 
#яка аналізує цей файл і повертає загальну та
# середню суму з/п всіх розробників

from decimal import Decimal

def total_salary(path: str) -> tuple [Decimal, Decimal]: # 1 аргумент
    total = 0.0
    count = 0

    try:
        with open(path, 'r', encoding = 'utf-8') as file: #менеджео контексту + кодування
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line: 
                    continue

                _, sal_str = line.split(',', 1)
                
                try:
                    salary = float(sal_str)
                except ValueError:
                    raise ValueError(f"Invalid salary value '{sal_str}' at line {line_number}")

                total += salary #обчислення загальної з/п
                count += 1

            if count == 0:
                raise ValueError("File contains no valid records")

            count_dec = Decimal(count)
            total_dec = Decimal(str(total))
            average_dec = total_dec/count_dec #точна середня з/п
            return total salary, average salary #кортеж створює кома

#опрацювання винятків при роботі з файлами
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except OSError as error:
        raise OSError(f"File error: {error}")

            

                    