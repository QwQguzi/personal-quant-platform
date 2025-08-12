import numpy as np

def backtest_single(close, signal, initial_capital, fee_perc, trading_days=252):
    pos = signal.shift(1).fillna(0).astype(float)
    returns = close.pct_change().fillna(0).astype(float)
    strat_ret = pos * returns
    trades = pos.diff().abs().fillna(0)
    cost = trades * fee_perc
    net_ret = strat_ret - cost
    equity = (1 + net_ret).cumprod() * initial_capital

    total_return = equity.iloc[-1] / equity.iloc[0] - 1
    ndays = len(net_ret.dropna())
    if ndays > 1:
        annual_return = (1 + net_ret).prod() ** (trading_days / ndays) - 1
        sharpe = net_ret.mean() / (net_ret.std(ddof=0) + 1e-9) * np.sqrt(trading_days)
    else:
        annual_return = np.nan
        sharpe = np.nan

    max_dd = (equity.cummax() - equity).max()

    return {
        "equity": equity,
        "net_ret": net_ret,
        "strat_ret": strat_ret,
        "trades": trades,
        "cost": cost,
        "total_return": total_return,
        "annual_return": annual_return,
        "sharpe": sharpe,
        "max_dd": max_dd
    }
