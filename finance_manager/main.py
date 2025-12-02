import sys
import os

from app.app import FinanceApp


def main():
    """Главная функция приложения"""
    try:
        app = FinanceApp()
        app.run()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
