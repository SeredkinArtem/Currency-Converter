import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# --- Конфигурация ---
API_KEY = "YOUR_API_KEY"  # Замените на ваш ключ
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"
HISTORY_FILE = "conversion_history.json"

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("500x400")
        
        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"] # Основные валюты
        self.history = self.load_history()
        
        self.create_widgets()
        self.update_history_display()

    def get_exchange_rate(self, from_currency):
        """Получение курса валют с внешнего API"""
        try:
            response = requests.get(API_URL + from_currency)
            data = response.json()
            if response.status_code == 200 and data.get('result') == 'success':
                return data['conversion_rates']
            else:
                messagebox.showerror("Ошибка API", data.get('error-type', "Неизвестная ошибка"))
                return None
        except Exception as e:
            messagebox.showerror("Ошибка сети", f"Не удалось подключиться к серверу: {e}")
            return None

    def convert_currency(self):
        """Логика конвертации"""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return

        rates = self.get_exchange_rate(from_curr)
        if rates and to_curr in rates:
            result = amount * rates[to_curr]
            
            # Сохранение в историю
            conversion = {
                "from": from_curr,
                "to": to_curr,
                "amount": amount,
                "result": result,
                "rate": rates[to_curr]
            }
            self.history.append(conversion)
            self.save_history()
            
            # Обновление интерфейса
            self.result_label.config(text=f"Результат: {result:.2f} {to_curr}")
            self.update_history_display()
        else:
            messagebox.showerror("Ошибка", f"Не удалось найти курс для {to_curr} или произошла ошибка запроса.")

    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self):
        """Сохранение истории в JSON"""
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def update_history_display(self):
        """Обновление таблицы истории"""
        for i in self.history_treeview.get_children():
            self.history_treeview.delete(i)
        for conv in self.history:
            self.history_treeview.insert('', 'end', values=(
                conv['from'],
                conv['to'],
                conv['amount'],
                conv['rate'],
                conv['result']
            ))

    def create_widgets(self):
        # --- Блок конвертации ---
        main_frame = tk.LabelFrame(self.root, text="Конвертация")
        main_frame.pack(padx=10, pady=10, fill=tk.X)

        # Валюта "Из"
        tk.Label(main_frame, text="Из:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.from_currency = tk.StringVar(value="USD")
        ttk.Combobox(main_frame, textvariable=self.from_currency,
                     values=self.currencies, state="readonly").grid(row=0, column=1, padx=5, pady=5)

         # Валюта "В"
         tk.Label(main_frame, text="В:").grid(row=0, column=2, sticky='e', padx=5, pady=5)
         self.to_currency = tk.StringVar(value="EUR")
         ttk.Combobox(main_frame, textvariable=self.to_currency,
                      values=self.currencies, state="readonly").grid(row=0, column=3, padx=5, pady=5)

         # Сумма
         tk.Label(main_frame, text="Сумма:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
         self.amount_entry = tk.Entry(main_frame)
         self.amount_entry.grid(row=1, column=1, columnspan=3, sticky='we', padx=5, pady=5)
         main_frame.grid_columnconfigure(1, weight=1) # Растяжение поля ввода

         # Кнопка и результат
         tk.Button(main_frame, text="Конвертировать", command=self.convert_currency).grid(row=2, column=0, columnspan=4, pady=10)
         
         self.result_label = tk.Label(main_frame, text="Результат: ", font=('Arial', 12))
         self.result_label.grid(row=3, column=0, columnspan=4)

         # --- Блок истории ---
         history_frame = tk.LabelFrame(self.root, text="История конвертаций")
         history_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)
         
         columns = ("Из", "В", "Сумма", "Курс", "Результат")
         self.history_treeview = ttk.Treeview(history_frame, columns=columns, show='headings')
         
         for col in columns:
             self.history_treeview.heading(col, text=col)
             self.history_treeview.column(col, anchor='center')
         
         scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_treeview.yview)
         self.history_treeview.configure(yscrollcommand=scrollbar.set)
         
         self.history_treeview.pack(side="left", fill="both", expand=True)
         scrollbar.pack(side="right", fill="y")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
