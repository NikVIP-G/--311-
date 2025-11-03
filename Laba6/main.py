import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import math

import hard_exp_with_ML as hard_exp


def first_exp():
    # Исходные данные: Фаренгейт -> Кельвины
    fahrenheit = np.array([-40, -22, -4, 14, 32, 50, 68, 86, 104, 122, 140, 158, 176, 194, 212])
    kelvin = (fahrenheit - 32) * 5 / 9 + 273.15  # Формула перевода

    print("Фаренгейт:", fahrenheit)
    print("Кельвины:", kelvin)

    # Визуализация
    plt.figure(figsize=(10, 6))
    plt.scatter(fahrenheit, kelvin, color='red', marker='o', label='F to K данные')
    plt.xlabel('Фаренгейт (°F)')
    plt.ylabel('Кельвины (K)')
    plt.title('Перевод из Фаренгейта в Кельвины')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Линейная регрессия
    fahrenheit_reshaped = fahrenheit.reshape(-1, 1)
    model = LinearRegression()
    model.fit(fahrenheit_reshaped, kelvin)

    # Предсказание
    fahrenheit_test = np.array([0, 100, 200]).reshape(-1, 1)
    kelvin_pred = model.predict(fahrenheit_test)

    print("Предсказанные значения:")
    for f, k in zip(fahrenheit_test.flatten(), kelvin_pred):
        print(f"{f}°F = {k:.2f}K")

    # Сравнение с реальными значениями
    kelvin_real = (fahrenheit_test.flatten() - 32) * 5 / 9 + 273.15
    print("\nРеальные значения:")
    for f, k in zip(fahrenheit_test.flatten(), kelvin_real):
        print(f"{f}°F = {k:.2f}K")


def second_exp():
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    categories = ['A', 'B', 'C', 'D']
    values = [23, 45, 56, 78]

    plt.figure(figsize=(15, 4))

    plt.subplot(1, 3, 1)
    plt.bar(categories, values, color=['red', 'blue', 'green', 'orange'])
    plt.title('Столбчатая диаграмма')
    plt.xlabel('Категории')
    plt.ylabel('Значения')

    plt.subplot(1, 3, 2)
    plt.pie(values, labels=categories, autopct='%1.1f%%', colors=['red', 'blue', 'green', 'orange'])
    plt.title('Круговая диаграмма')

    plt.subplot(1, 3, 3)
    plt.fill_between(x, y1, alpha=0.5, label='sin(x)')
    plt.fill_between(x, y2, alpha=0.5, label='cos(x)')
    plt.title('График с заполнением')
    plt.legend()

    plt.tight_layout()
    plt.show()


def third_exp():
    journal_number = 2
    phone_memory_gb = 256

    print("Число Эйлера (e):", math.e)
    print("Число Пи (π):", math.pi)
    print("NaN:", math.nan)
    print(f"Факториал {journal_number}:", math.factorial(journal_number))
    print(f"Наибольший общий делитель {journal_number} и {phone_memory_gb}:",
          math.gcd(journal_number, phone_memory_gb))


def forth_exp():
    theta = np.linspace(0, 2 * np.pi, 1000)

    r = np.sin(5 * theta) * np.cos(4 * theta) + 1

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, color='red', linewidth=3, label='Цветок')
    plt.fill(x, y, alpha=0.3, color='pink')

    plt.plot([0, 0], [min(y) - 0.5, min(y)], color='green', linewidth=4, label="Стебель")  # Стебель

    leaf_x = np.linspace(-0.5, 0.5, 100)
    leaf_y = -0.2 * (leaf_x ** 2) + min(y) - 0.2
    plt.plot(leaf_x, leaf_y, color='green', linewidth=3)

    plt.title('Сложная фигура: Цветок')
    plt.axis('equal')
    plt.axis('off')
    plt.legend()
    plt.show()


def main():
    while True:
        user_input = input("Введите команду: ")

        match user_input:
            case "1":
                first_exp()
            case "2":
                second_exp()
            case "3":
                third_exp()
            case "4":
                forth_exp()
            case "5":
                hard_exp.run()
            case "0":
                break
            case _:
                print("Такой команды нет!")

        print()


if __name__ == "__main__":
    main()
