def calc_momentum(close, window):
    return close.pct_change(periods=window)

def time_series_zscore(s, window):
    roll_mean = s.rolling(window=window, min_periods=1).mean()
    roll_std = s.rolling(window=window, min_periods=1).std(ddof=0).fillna(0) + 1e-9
    return (s - roll_mean) / roll_std