import numpy as np
import pandas as pd

def calculate_risk_metrics(equity, net_ret, trading_days=252):
    """
    计算风险指标
    
    Args:
        equity: 净值曲线
        net_ret: 净收益率序列
        trading_days: 年交易日数
        
    Returns:
        包含各项风险指标的字典
    """
    # 处理零值和空值
    if len(equity) == 0 or len(net_ret) == 0:
        return {
            "volatility": 0,
            "max_drawdown": 0,
            "annual_return": 0,
            "sharpe": 0,
            "win_rate": 0,
            "profit_factor": 0
        }
    
    # 计算波动率
    volatility = net_ret.std() * np.sqrt(trading_days)
    
    # 计算最大回撤
    max_dd = (equity.cummax() - equity) / equity.cummax()
    
    # 计算总收益率和年化收益率
    total_return = equity.iloc[-1] / equity.iloc[0] - 1
    n_years = max(len(equity) / trading_days, 1e-6)  # 避免除零
    annual_return = (1 + total_return) ** (1 / n_years) - 1
    
    # 计算夏普比率
    ret_std = net_ret.std()
    if ret_std == 0:
        sharpe = 0
    else:
        sharpe = net_ret.mean() / ret_std * np.sqrt(trading_days)
    
    # 计算盈亏比
    wins = net_ret[net_ret > 0]
    losses = net_ret[net_ret < 0]
    profit_factor = abs(wins.sum() / (losses.sum() + 1e-9))
    
    return {
        "volatility": volatility,
        "max_drawdown": max_dd.max(),
        "annual_return": annual_return,
        "sharpe": sharpe,
        "win_rate": (net_ret > 0).mean(),
        "profit_factor": profit_factor
    }

def apply_stop_loss(pos, returns, stop_loss=-0.05):
    """
    应用止损
    
    Args:
        pos: 持仓序列
        returns: 收益率序列
        stop_loss: 止损比例，默认-5%
    """
    position = pos.copy()
    cum_returns = (1 + returns).cumprod()
    entry_price = None
    
    for i in range(1, len(position)):
        if position[i] != 0:  # 有持仓
            if entry_price is None:
                entry_price = cum_returns[i]
            # 计算浮动盈亏
            floating_pnl = cum_returns[i] / entry_price - 1
            # 触发止损
            if floating_pnl < stop_loss:
                position[i:] = 0
                entry_price = None
        elif position[i] == 0 and position[i-1] != 0:  # 清仓
            entry_price = None
            
    return position

def backtest_single(close, signal, initial_capital, fee_perc, trading_days=252, 
                   position_size=0.7, stop_loss=-0.05):
    """
    单策略回测
    
    Args:
        close: 收盘价序列
        signal: 信号序列 (1: 买入, -1: 卖出, 0: 持仓)
        initial_capital: 初始资金
        fee_perc: 交易费率
        trading_days: 年交易日数
        position_size: 仓位比例，默认0.7（即70%仓位）
        stop_loss: 止损比例，默认-5%
    
    Returns:
        包含回测结果的字典
    """
    try:
        # 将信号转换为实际仓位
        pos = signal.shift(1).fillna(0).astype(float) * position_size
        
        # 计算收益率
        returns = close.pct_change().fillna(0).astype(float)
        
        # 应用止损
        if stop_loss is not None:
            pos = apply_stop_loss(pos, returns, stop_loss)
        
        # 计算策略收益
        strat_ret = pos * returns
        
        # 计算交易成本
        trades = pos.diff().abs().fillna(0)
        cost = trades * fee_perc
        
        # 计算净收益
        net_ret = strat_ret - cost
        
        # 计算净值曲线
        equity = pd.Series((1 + net_ret).cumprod() * initial_capital)
        
        # 计算交易统计
        trade_count = (trades > 0).sum()
        avg_trade_return = net_ret[trades > 0].mean()
        avg_hold_days = (pos != 0).sum() / max(1, (pos != 0).astype(int).diff().abs().sum()/2)
        
        # 计算风险指标
        risk_metrics = calculate_risk_metrics(equity, net_ret, trading_days)
        
        return {
            "equity": equity,
            "total_return": equity.iloc[-1] / initial_capital - 1,
            "annual_return": risk_metrics["annual_return"],
            "sharpe": risk_metrics["sharpe"],
            "max_drawdown": risk_metrics["max_drawdown"],
            "win_rate": risk_metrics["win_rate"],
            "profit_factor": risk_metrics["profit_factor"],
            "trade_count": trade_count,
            "avg_trade_return": avg_trade_return,
            "avg_hold_days": avg_hold_days,
            "volatility": risk_metrics["volatility"]
        }
        
    except Exception as e:
        print(f"回测过程中出错: {str(e)}")
        return None