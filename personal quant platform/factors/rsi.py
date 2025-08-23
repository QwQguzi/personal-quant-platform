import pandas as pd
import numpy as np

def calc_rsi(prices, period=28):
    """计算RSI指标
    
    Args:
        prices: 收盘价序列
        period: RSI计算周期，默认14天
    
    Returns:
        RSI指标值序列
    """
    # 计算价格变化
    delta = prices.diff()
    
    # 分别获取上涨和下跌
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # 计算RS和RSI
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi