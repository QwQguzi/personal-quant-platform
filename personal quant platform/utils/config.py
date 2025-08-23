from pathlib import Path

INPUT_CSV = Path("data/factor_data/example_long.csv")
OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

INITIAL_CAPITAL = 1_000_000
FEE_PERC = 0.0003
MOM_WINDOW = 63
VOL_WINDOW = 20
MA_SHORT = 5
MA_LONG = 20
TRADING_DAYS = 252
