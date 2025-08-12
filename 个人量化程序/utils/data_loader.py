import pandas as pd

def load_single_stock_data(filepath):
    df = pd.read_csv(filepath, encoding="utf-8-sig", dtype=str)
    col_map = {}
    if "date" in df.columns:
        col_map["date"] = "date"
    elif "日期" in df.columns:
        col_map["日期"] = "date"

    if "股票代码" in df.columns:
        col_map["股票代码"] = "code"
    elif "code" in df.columns:
        col_map["code"] = "code"

    if "close" in df.columns:
        col_map["close"] = "close"
    elif "收盘" in df.columns:
        col_map["收盘"] = "close"
    elif "close_price" in df.columns:
        col_map["close_price"] = "close"

    df = df.rename(columns=col_map)
    if not {"date", "close"}.issubset(df.columns):
        raise ValueError("CSV 必须包含 date 和 close 列")

    if "code" in df.columns:
        codes = df["code"].unique()
        if len(codes) > 1:
            df = df[df["code"] == codes[0]]

    df["date"] = pd.to_datetime(df["date"])
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)

    return df.set_index("date")["close"]

print("data_loader.py loaded")