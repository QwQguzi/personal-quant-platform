import pandas as pd

def generate_signal_ma(close, ma_short, ma_long):
    """
    均线交叉策略信号：
    - 短均线上穿长均线 -> 买入信号 (1)
    - 短均线下穿长均线 -> 卖出信号 (-1)
    - 其它情况 -> 0
    """
    ma_s = close.rolling(window=ma_short, min_periods=1).mean()
    ma_l = close.rolling(window=ma_long, min_periods=1).mean()

    signal = pd.Series(0, index=close.index)

    for i in range(1, len(close)):
        # 上穿：前一日短均线 <= 长均线，今日短均线 > 长均线
        if ma_s.iloc[i-1] <= ma_l.iloc[i-1] and ma_s.iloc[i] > ma_l.iloc[i]:
            signal.iloc[i] = 1
        # 下穿：前一日短均线 >= 长均线，今日短均线 < 长均线
        elif ma_s.iloc[i-1] >= ma_l.iloc[i-1] and ma_s.iloc[i] < ma_l.iloc[i]:
            signal.iloc[i] = -1

    return signal
