import matplotlib.pyplot as plt

def plot_price_signals(close, signal, title, filename):
    buys = signal[(signal.diff() == 1)].index
    sells = signal[(signal.diff() == -1)].index

    plt.figure(figsize=(12,6))
    plt.plot(close.index, close.values, label="Close Price", color='black')
    plt.scatter(buys, close.reindex(buys), marker='^', color='green', label='Buy Signal', s=100, zorder=5)
    plt.scatter(sells, close.reindex(sells), marker='v', color='red', label='Sell Signal', s=100, zorder=5)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"保存买卖点图到 {filename}")
