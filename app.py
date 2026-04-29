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

      
