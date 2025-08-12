from utils.config import *
from utils.data_loader import load_single_stock_data
from factors.momentum import calc_momentum, time_series_zscore
from strategies.momentum_strategy import generate_signal_momentum
from strategies.moving_average import generate_signal_ma
from backtest.engine import backtest_single
from utils.plot import plot_price_signals
from pathlib import Path
from utils.data_loader import load_single_stock_data
from utils.data_loader import load_single_stock_data
from utils.config import INPUT_CSV

def safe_window(w, n):
    return min(max(2, w), max(2, n//2 if n//2 >= 2 else n))

def main():
    close = load_single_stock_data(INPUT_CSV)
    n = len(close)
    print(f"样本长度（交易日）：{n}")

    mom_w = safe_window(MOM_WINDOW, n)
    vol_w = safe_window(VOL_WINDOW, n)
    ma_s = min(MA_SHORT, max(1, n-1))
    ma_l = min(MA_LONG, max(ma_s+1, n-1))
    print(f"使用窗口：MOM_WINDOW={mom_w}, VOL_WINDOW={vol_w}, MA_SHORT={ma_s}, MA_LONG={ma_l}")

    momentum = calc_momentum(close, mom_w)
    mom_z = time_series_zscore(momentum, mom_w)

    signal_mom = generate_signal_momentum(mom_z)
    signal_ma = generate_signal_ma(close, ma_s, ma_l)

    out_mom = backtest_single(close, signal_mom, INITIAL_CAPITAL, FEE_PERC, TRADING_DAYS)
    out_ma = backtest_single(close, signal_ma, INITIAL_CAPITAL, FEE_PERC, TRADING_DAYS)

    OUT_DIR.mkdir(exist_ok=True)
    out_mom["equity"].to_csv(OUT_DIR / "equity_mom.csv", encoding="utf-8-sig")
    out_ma["equity"].to_csv(OUT_DIR / "equity_ma.csv", encoding="utf-8-sig")

    plot_price_signals(close, signal_mom, "动量策略买卖点", OUT_DIR / "price_signal_mom.png")
    plot_price_signals(close, signal_ma, "均线策略买卖点", OUT_DIR / "price_signal_ma.png")

    print("\n=== 结果 ===")
    print("Momentum strategy: total_return={:.2%}, annual_return={:.2%}, sharpe={:.2f}, max_dd={:.2f}".format(
        out_mom["total_return"], out_mom["annual_return"] if out_mom["annual_return"] is not None else 0, out_mom["sharpe"], out_mom["max_dd"]))
    print("MA crossover   : total_return={:.2%}, annual_return={:.2%}, sharpe={:.2f}, max_dd={:.2f}".format(
        out_ma["total_return"], out_ma["annual_return"] if out_ma["annual_return"] is not None else 0, out_ma["sharpe"], out_ma["max_dd"]))

    print(f"\n生成文件保存在 {OUT_DIR.resolve()}/")

if __name__ == "__main__":
    main()
