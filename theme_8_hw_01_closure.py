#Треба:реалізувати функцію caching_fibonacci (рекурсивно):
#створює та використовує кеш для зберігання й
#повторного використання вже обчислених значень чисел Фібоначчі 


def caching_fibonacci(): #фабрика функції з замиканням
    cache = {}

    def fibonacci(n):
        if n in cache:
            return cache[n]

        if n <= 1:
            return n

        result = fibonacci(n - 1) + fibonacci(n - 2)
        cache[n] = result
        return result

    return fibonacci