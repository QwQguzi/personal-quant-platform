def generate_signal_ma(close, ma_short, ma_long):
    ma_s = close.rolling(window=ma_short, min_periods=1).mean()
    ma_l = close.rolling(window=ma_long, min_periods=1).mean()
    signal = (ma_s > ma_l).astype(int).fillna(0)
    return signal
