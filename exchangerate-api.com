import requests

def get_rate(from_currency, to_currency, api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["conversion_rate"]
