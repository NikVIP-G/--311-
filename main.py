def input_digit(text_input: str = "Введите число: ") -> int:
    n = input(text_input)

    check_num = n if n[0] != '-' else n[1:]

    while not check_num.isdigit():
        print("Надо ввести число!")
        print()
        n = input(text_input)

    return int(n)


def input_float(text_input: str = "Введите число: ") -> float:
    n = input(text_input)

    def is_float(n: str):
        try:
            float(n)
            return True
        except ValueError:
            return False

    while not is_float(n):
        print("Надо ввести дейтсвительное число!")
        n = input(text_input)

    return float(n)


def is_year_leap(year: int) -> bool:
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False


def is_prime(n: int) -> bool:
    for i in range(2, n//2 + 1):
        if n % i == 0:
            return False

    return True


def first_exp():
    print('-' * 10 + 'Задание 1' + '-' * 10)

    calendar = {
        '1': "январь",
        '2': "февраль",
        '3': "март",
        '4': "апрель",
        '5': "май",
        '6': "июнь",
        '7': "июль",
        '8': "август",
        '9': "сентабрь",
        '10': "октябрь",
        '11': "ноябрь",
        '12': "декабрь"
    }

    n = input("Введите номер месяца, который хотите вывести: ")
    if n in calendar.keys():
        print(calendar[n])
    else:
        first_exp()


def second_exp():
    print('-' * 10 + 'Задание 2' + '-' * 10)

    n = input_digit()

    if n % 2 == 0:
        print("Число четное")
    else:
        print("Число нечетное")


def third_exp():
    print('-' * 10 + 'Задание 3' + '-' * 10)

    n = input_digit()

    if n > 40:
        print("stonks")
    else:
        print("not stonks")


def forth_exp():
    print('-' * 10 + 'Задание 4' + '-' * 10)

    year = input_digit("Введите год: ")

    if is_year_leap(year):
        print("Високосный")
    else:
        print("Не вискоксный")


def fifth_exp():
    print('-' * 10 + 'Задание 5' + '-' * 10)

    n = input_digit()

    if is_prime(n):
        print("Простое число!")
    else:
        print("Не простое число!")


def sixth_exp():
    print('-' * 10 + 'Задание 6' + '-' * 10)

    a = input_float("Введите первое число: ")
    b = input_float("Введите второе число: ")

    r = (-138 / 2) ** 1.3
    r = r.real

    if a / b == 3.6 or (r <= b <= (-69 / 28 ** 5.1) * 4):
        a, b = b, a
        print("Переменные поменяли местами")
    else:
        print("Переменные не менялись местами")

    print()
    print(f"a = {a}; b = {b}")


def seventh_exp():
    print('-' * 10 + 'Задание 7' + '-' * 10)

    unique = set()
    c_even = 0
    c_negative = 0
    c_in_range = 0

    n = 0

    while n != 5:
        a = input_digit(f"Введите {n + 1} число: ")
        n += 1

        unique.add(a)

        if a % 2 == 0:
            c_even += 1

        if a < 0:
            c_negative += 1

        if a in range(-256, 1024 + 1):
            c_in_range += 1

    print(f"Количество уникальных = {len(unique)};\n"
          f"Количество четных = {c_even}\n"
          f"Количество отрицательных = {c_negative}\n"
          f"Количество чисел в диапозоне [-256, 1024] = {c_in_range}")


def special_exp():
    print('-' * 10 + 'Задание повышенной сложности' + '-' * 10)

    a = input_digit("a = ")
    b = input_digit("b = ")
    c = input_digit("c = ")

    res = ((a**2 + b**3)/(c + 3)) / 4

    print(res, end='')

    if res % 2 == 0:
        print(" - четное")
    else:
        print(" - нечетное")


if __name__ == "__main__":
    is_work = True

    while is_work:
        user_input = input("Введите номер задания 1-8 (0 - выход из программы): ")

        match user_input:
            case '1':
                first_exp()
            case '2':
                second_exp()
            case '3':
                third_exp()
            case '4':
                forth_exp()
            case '5':
                fifth_exp()
            case '6':
                sixth_exp()
            case '7':
                seventh_exp()
            case '8':
                special_exp()
            case '0':
                is_work = False
            case _:
                print("Такой команды не существует!")

        print()
