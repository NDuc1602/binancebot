# BinanceBot Training Data (2020-2025)

## Description
Historical OHLCV data for cryptocurrency trading bot training.

## Contents
- **Pairs**: BTC/USDT, ETH/USDT, BNB/USDT
- **Timeframes**: 4h, 12h, 1d
- **Period**: 2020-01-01 to 2025-11-22 (~6 years)
- **Files**: 9 JSON files
- **Format**: BinanceBot compatible format

## Usage in Kaggle Notebook

```python
import shutil
from pathlib import Path

# Copy data to working directory
dataset_path = Path('/kaggle/input/binancebot-data-2020-2025/data')
target_path = Path('/kaggle/working/user_data/data')

target_path.mkdir(parents=True, exist_ok=True)
shutil.copytree(dataset_path, target_path, dirs_exist_ok=True)

print("✓ Data copied successfully!")
```

## Data Structure
```
data/
└── binance/
    ├── BTC_USDT-4h.json
    ├── BTC_USDT-12h.json
    ├── BTC_USDT-1d.json
    ├── ETH_USDT-4h.json
    ├── ETH_USDT-12h.json
    ├── ETH_USDT-1d.json
    ├── BNB_USDT-4h.json
    ├── BNB_USDT-12h.json
    └── BNB_USDT-1d.json
```

Generated: 2025-11-23 16:57:00
