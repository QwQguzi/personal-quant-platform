from utils.config import *
from factors.momentum import calc_momentum, time_series_zscore
from strategies.momentum_strategy import generate_signal_momentum
from strategies.moving_average import generate_signal_ma
from backtest.engine import backtest_single
from utils.plot import plot_price_signals
from strategies.volume_strategy import generate_signal_volume
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# 在文件开头添加导入
from factors.rsi import calc_rsi
from strategies.rsi_strategy import generate_signal_rsi

def safe_window(w, n):
    return min(max(2, w), max(2, n//2 if n//2 >= 2 else n))

def load_clean_csv(filepath):
    # 跳过第二行（header后面的那一行）
    return pd.read_csv(filepath, skiprows=[1])

def plot_kline(df, root, title="K线图"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["date"], df["close"], label="收盘价", color="blue")
    ax.set_title(title)
    ax.set_xlabel("日期")
    ax.set_ylabel("收盘价")
    ax.legend()
    fig.autofmt_xdate()
    # 清理旧图
    for widget in root.pack_slaves():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def run_selected_strategies(selected, csv_path):
    df = load_clean_csv(csv_path)
    close = df["close"]
    volume = df["volume"]
    n = len(close)
    mom_w = safe_window(MOM_WINDOW, n)
    vol_w = safe_window(VOL_WINDOW, n)
    ma_s = min(MA_SHORT, max(1, n-1))
    ma_l = min(MA_LONG, max(ma_s+1, n-1))
    OUT_DIR.mkdir(exist_ok=True)
    results = []
    if "momentum" in selected:
        momentum = calc_momentum(close, mom_w)
        mom_z = time_series_zscore(momentum, mom_w)
        signal_mom = generate_signal_momentum(mom_z)
        out_mom = backtest_single(close, signal_mom, INITIAL_CAPITAL, FEE_PERC, TRADING_DAYS)
        out_mom["equity"].to_csv(OUT_DIR / "equity_mom.csv", encoding="utf-8-sig")
        plot_price_signals(close, signal_mom, "动量策略买卖点", OUT_DIR / "price_signal_mom.png")
        results.append(f"Momentum: total_return={out_mom['total_return']:.2%}, sharpe={out_mom['sharpe']:.2f}")
    if "ma" in selected:
        signal_ma = generate_signal_ma(close, ma_s, ma_l)
        out_ma = backtest_single(close, signal_ma, INITIAL_CAPITAL, FEE_PERC, TRADING_DAYS)
        out_ma["equity"].to_csv(OUT_DIR / "equity_ma.csv", encoding="utf-8-sig")
        plot_price_signals(close, signal_ma, "均线策略买卖点", OUT_DIR / "price_signal_ma.png")
        results.append(f"MA: total_return={out_ma['total_return']:.2%}, sharpe={out_ma['sharpe']:.2f}")
    if "volume" in selected:
        signal_vol = generate_signal_volume(volume, window=VOL_WINDOW, threshold=2.0)
        out_vol = backtest_single(close, signal_vol, INITIAL_CAPITAL, FEE_PERC, TRADING_DAYS)
        out_vol["equity"].to_csv(OUT_DIR / "equity_volume.csv", encoding="utf-8-sig")
        plot_price_signals(close, signal_vol, "成交量策略买卖点", OUT_DIR / "price_signal_volume.png")
        results.append(f"Volume: total_return={out_vol['total_return']:.2%}, sharpe={out_vol['sharpe']:.2f}")
    if "rsi" in selected:
        rsi = calc_rsi(close, period=14)
        signal_rsi = generate_signal_rsi(rsi)
        out_rsi = backtest_single(close, signal_rsi, INITIAL_CAPITAL, FEE_PERC, TRADING_DAYS)
        out_rsi["equity"].to_csv(OUT_DIR / "equity_rsi.csv", encoding="utf-8-sig")
        plot_price_signals(close, signal_rsi, "RSI策略买卖点", OUT_DIR / "price_signal_rsi.png")
        results.append(f"RSI: total_return={out_rsi['total_return']:.2%}, sharpe={out_rsi['sharpe']:.2f}")
    return results

def main():
    root = tk.Tk()
    root.title("策略选择与回测")
    tk.Label(root, text="请选择要运行的策略：").pack()
    var_mom = tk.BooleanVar()
    var_ma = tk.BooleanVar()
    var_vol = tk.BooleanVar()
    var_rsi = tk.BooleanVar()
    tk.Checkbutton(root, text="RSI策略(rsi)", variable=var_rsi).pack(anchor="w")
    tk.Checkbutton(root, text="动量策略(momentum)", variable=var_mom).pack(anchor="w")
    tk.Checkbutton(root, text="均线策略(ma)", variable=var_ma).pack(anchor="w")
    tk.Checkbutton(root, text="成交量策略(volume)", variable=var_vol).pack(anchor="w")
    result_label = tk.Label(root, text="", fg="blue")
    result_label.pack()
    csv_path = tk.StringVar()
    df_cache = {}

    def select_file():
        path = filedialog.askopenfilename(title="选择CSV数据文件", filetypes=[("CSV文件", "*.csv")])
        if path:
            csv_path.set(path)
            result_label.config(text=f"已选择文件：{path}")
            df = load_clean_csv(path)
            df_cache["df"] = df
            plot_kline(df, root, title=f"{df['股票代码'].iloc[0]} K线图")

    def on_run():
        selected = []
        if var_mom.get(): selected.append("momentum")
        if var_ma.get(): selected.append("ma")
        if var_vol.get(): selected.append("volume")
        if var_rsi.get(): selected.append("rsi") 
        if not selected:
            messagebox.showwarning("提示", "请至少选择一个策略！")
            return
        if not csv_path.get():
            messagebox.showwarning("提示", "请先选择数据文件！")
            return
        results = run_selected_strategies(selected, csv_path.get())
        result_label.config(text="\n".join(results) + f"\n结果文件保存在 {OUT_DIR.resolve()}/")

    tk.Button(root, text="选择数据文件", command=select_file).pack(pady=5)
    tk.Button(root, text="运行回测", command=on_run).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
