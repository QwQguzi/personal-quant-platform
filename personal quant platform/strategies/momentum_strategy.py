import pandas as pd

def generate_signal_momentum(mom_z: pd.Series) -> pd.Series:
    """
    动量策略信号：
    - mom_z 从负转正 -> 买入 (1)
    - mom_z 从正转负 -> 卖出 (-1)
    - 其它情况 -> 0
    """
    signal = pd.Series(0, index=mom_z.index)

    for i in range(1, len(mom_z)):
        if mom_z.iloc[i-1] <= 0 and mom_z.iloc[i] > 0:
            signal.iloc[i] = 1
        elif mom_z.iloc[i-1] >= 0 and mom_z.iloc[i] < 0:
            signal.iloc[i] = -1

    return signal
