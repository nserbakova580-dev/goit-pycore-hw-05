#Треба:реалізувати функцію caching_fibonacci (рекурсивно):
#створює та використовує кеш для зберігання й
#повторного використання вже обчислених значень чисел Фібоначчі 


def caching_fibonacci(func): #паттерн memoization через власний декоратор
    cache = {}

    def wrapper(n):

        if n in cache:
            return cache[n]

        result = func(n)
        cache[n] = result

        return result

    return wrapper


@caching_fibonacci
def fibonacci(n):

    if n <= 1:
        return n 
        
    return fibonacci(n - 1) + fibonacci(n - 2)
  

   