def filter_and_sort(numbers):
    # Ошибка 1: нет проверки типа input
    # Ошибка 2: не проверяет, что все элементы - integers
    # Ошибка 3: сортирует по убыванию вместо возрастания
    filtered = [n for n in numbers if n >= 0]
    return sorted(filtered, reverse=True)  # reverse=True → неправильная сортировка
