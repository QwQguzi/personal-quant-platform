import numpy as np
import pandas as pd

def generate_signal_rsi(rsi, overbought=75, oversold=25):
    """基于RSI生成交易信号：1=买入, -1=卖出, 0=空仓，确保第一个信号是买入"""
    rsi = pd.Series(rsi) if isinstance(rsi, np.ndarray) else rsi
    signals = pd.Series(0, index=rsi.index)

    # 检查 RSI 上一时刻和当前时刻，判断是否突破阈值
    for i in range(1, len(rsi)):
        # 下穿 oversold → 生成买入信号
        if rsi[i-1] >= oversold and rsi[i] < oversold:
            signals[i] = 1
        # 上穿 overbought → 生成卖出信号
        elif rsi[i-1] <= overbought and rsi[i] > overbought:
            signals[i] = -1

    # 确保第一个信号是买入
    first_nonzero = signals[signals != 0].index.min()
    if first_nonzero is not None and signals[first_nonzero] == -1:
        signals[first_nonzero] = 0  # 忽略第一个卖出信号

    return signals
