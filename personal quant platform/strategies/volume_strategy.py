# strategies/volume_strategy.py

import pandas as pd

def generate_signal_volume(volume: pd.Series, window: int = 20, threshold: float = 2.0) -> pd.Series:
    """
    生成成交量策略买卖信号：
    - 当成交量 > 最近 window 天均值 * threshold 时，触发买入信号 (1)
    - 当成交量 < 最近 window 天均值 时，触发卖出信号 (-1)
    - 其余时间为 0
    返回信号Series，索引与 volume 一致。
    """
    rolling_mean = volume.rolling(window=window, min_periods=1).mean()
    signal = pd.Series(0, index=volume.index)

    position = 0  # 当前持仓状态（0空仓，1持仓）
    for i in range(len(volume)):
        if position == 0 and volume.iloc[i] > rolling_mean.iloc[i] * threshold:
            signal.iloc[i] = 1   # 触发买入信号
            position = 1
        elif position == 1 and volume.iloc[i] < rolling_mean.iloc[i]:
            signal.iloc[i] = -1  # 触发卖出信号
            position = 0
        # 其它情况 signal 维持 0
    
    return signal
