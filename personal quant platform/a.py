import yfinance as yf
import pandas as pd
import os

# 示例：手动指定部分美股代码
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

qualified = []
for ticker in tickers:
    try:
        info = yf.Ticker(ticker).info
        market_cap = info.get("marketCap", 0)
        if market_cap and market_cap > 2e8:
            qualified.append(ticker)
    except Exception as e:
        print(f"{ticker} 获取市值失败: {e}")

print(f"市值大于2亿的股票数量: {len(qualified)}")

save_dir = "data/raw"
os.makedirs(save_dir, exist_ok=True)

for ticker in qualified:
    try:
        # 日线数据
        df_day = yf.download(ticker, start="2024-08-01", end="2025-08-01", interval="1d")
        if not df_day.empty:
            df_day = df_day.reset_index()
            df_day["股票代码"] = ticker
            df_day.rename(columns={
                "Date": "date",
                "Open": "open",
                "Close": "close",
                "High": "high",
                "Low": "low",
                "Volume": "volume"
            }, inplace=True)
            df_day = df_day[["date", "股票代码", "open", "close", "high", "low", "volume"]]
            df_day.to_csv(f"{save_dir}/{ticker}_day.csv", index=False, encoding="utf-8-sig")
            print(f"{ticker} 日线保存成功")

        # 15分钟线（只能最近7天）
        df_15m = yf.download(ticker, period="7d", interval="15m")
        if not df_15m.empty:
            df_15m = df_15m.reset_index()
            df_15m["股票代码"] = ticker
            df_15m.rename(columns={
                "Datetime": "date",
                "Open": "open",
                "Close": "close",
                "High": "high",
                "Low": "low",
                "Volume": "volume"
            }, inplace=True)
            df_15m = df_15m[["date", "股票代码", "open", "close", "high", "low", "volume"]]
            df_15m.to_csv(f"{save_dir}/{ticker}_15m.csv", index=False, encoding="utf-8-sig")
            print(f"{ticker} 15分钟线保存成功")
    except Exception as e:
        print(f"{ticker} 下载失败: {e}")