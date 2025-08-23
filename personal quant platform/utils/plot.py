import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

def plot_price_signals(price, signal, title, filename):
    """Draw price chart with buy/sell signals (date-aware)"""
    plt.figure(figsize=(12, 6))
    
    # 确保是Series并且索引一致
    price = pd.Series(price)
    signal = pd.Series(signal, index=price.index)

    # 如果索引是日期，就直接用；否则还是用range
    if pd.api.types.is_datetime64_any_dtype(price.index):
        x = price.index
    else:
        x = range(len(price))
    
    # 绘制价格线
    plt.plot(x, price.values, label='Close', color='black')
    
    # 绘制买入点
    buy_points = signal == 1
    if buy_points.any():
        plt.plot(price.index[buy_points], price[buy_points],
                 '^', color='red', markersize=10, label='Buy')
    
    # 绘制卖出点
    sell_points = signal == -1
    if sell_points.any():
        plt.plot(price.index[sell_points], price[sell_points],
                 'v', color='green', markersize=10, label='Sell')
    
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # 如果是时间序列，自动美化X轴
    if pd.api.types.is_datetime64_any_dtype(price.index):
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.gcf().autofmt_xdate(rotation=45)

    # 保存之前打印信号统计
    print(f"Total data points: {len(price)}")
    print(f"Signal points: {signal.value_counts().to_dict()}")
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Saved signal plot to {filename}")
