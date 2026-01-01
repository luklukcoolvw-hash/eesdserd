from iexfinance.stocks import Stock
from datetime import datetime

# Deinen API-Token hier einfügen
api_token = "DEIN_API_TOKEN"

# Beispiel: Apple-Aktie
symbol = "AAPL"
stock = Stock(symbol, token=api_token)

# Echtzeitpreis abrufen
quote = stock.get_quote()
price = quote['latestPrice']
time = datetime.fromtimestamp(quote['latestUpdate']/1000)

print(f"{symbol}: {price} USD um {time.strftime('%H:%M:%S')}")