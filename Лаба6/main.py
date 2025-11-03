import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import math


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
    ...


def main():
    user_input = input("Введите команду: ")

    match user_input:
        case "1":
            first_exp()
        case _:
            print("Такой команды нет!")


if __name__ == "__main__":
    main()
