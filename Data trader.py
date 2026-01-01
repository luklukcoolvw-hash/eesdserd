import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

ticker = "GC=F"  # Gold-Future

fig, ax = plt.subplots()
plt.title("Goldpreis Echtzeit-Chart")
plt.xlabel("Zeit")
plt.ylabel("Preis (USD/Unze)")

times = []
prices = []

def update(frame):
    global times, prices
    data = yf.download(ticker, period="1d", interval="1m")

    if data.empty:
        print("Keine Daten verfügbar – nächster Versuch")
        return

    current_time = data.index[-1]
    current_price = data['Close'].iloc[-1]

    times.append(current_time)
    prices.append(current_price)

    ax.clear()
    ax.plot(times[-30:], prices[-30:], marker='o')
    ax.set_title(f"Goldpreis Echtzeit-Chart\nLetzte Aktualisierung: {datetime.now().strftime('%H:%M:%S')}")
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Preis (USD/Unze)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

ani = FuncAnimation(fig, update, interval=60000)  # alle 60 Sekunden
plt.show()