import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import datetime

API_KEY = "ВАШ_API_КЛЮЧ"  # Замените на свой ключ с exchangerate-api.com
HISTORY_FILE = "history.json"

def get_rate(from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    data = response.json()
    if data.get("result") == "error":
        raise Exception(data.get("error-type"))
    return data["conversion_rate"]

def save_history(entry):
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def load_history(tree):
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
            for entry in history:
                tree.insert("", "end", values=(
                    entry["from"],
                    entry["to"],
                    entry["amount"],
                    round(entry["result"], 2),
                    round(entry["rate"], 4)
                ))
    except FileNotFoundError:
        pass

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
        return amount
    except ValueError:
        raise ValueError("Некорректный ввод суммы.")

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.currencies = ["USD", "EUR", "GBP", "RUB", "JPY"]

        ttk.Label(root, text="Из:").grid(row=0, column=0, padx=10, pady=5)
        self.from_currency = ttk.Combobox(root, values=self.currencies)
        self.from_currency.current(0)
        self.from_currency.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="В:").grid(row=1, column=0, padx=10, pady=5)
        self.to_currency = ttk.Combobox(root, values=self.currencies)
        self.to_currency.current(1)
        self.to_currency.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(root, text="Сумма:").grid(row=2, column=0, padx=10, pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        self.convert_button = ttk.Button(root, text="Конвертировать", command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.history_tree = ttk.Treeview(root, columns=("from", "to", "amount", "result", "rate"), show="headings")
        self.history_tree.heading("from", text="Из")
        self.history_tree.heading("to", text="В")
        self.history_tree.heading("amount", text="Сумма")
        self.history_tree.heading("result", text="Результат")
        self.history_tree.heading("rate", text="Курс")
        self.history_tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        load_history(self.history_tree)

    def convert(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        amount_str = self.amount_entry.get()

        try:
            amount = validate_amount(amount_str)
            rate = get_rate(from_curr, to_curr)
            result = amount * rate

            # Сохранение в историю
            entry = {
                "from": from_curr,
                "to": to_curr,
                "amount": amount,
                "result": result,
                "rate": rate,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_history(entry)

            # Отображение в таблице
            self.history_tree.insert("", "end", values=(
                from_curr,
                to_curr,
                amount,
                round(result, 2),
                round(rate, 4)
            ))
            messagebox.showinfo("Готово!", f"Результат: {round(result, 2)} {to_curr}")

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка API", f"Не удалось получить курс: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
