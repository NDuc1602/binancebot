"""
Kaggle Training Script for UniversalMACD Strategy
Chạy hyperopt với 300 epochs cho 3 timeframes

Hướng dẫn:
1. Tạo Kaggle Notebook
2. Copy toàn bộ file này vào notebook
3. Chạy từng cell
4. Download kết quả từ Output tab
"""

# ===== CELL 1: Setup & Install =====
# Cài đặt BinanceBot từ uploaded dataset
import subprocess
import sys
import os

print("Installing BinanceBot from uploaded package...")

# NOTE: Thay 'binancebot-package' bằng tên dataset bạn đã upload
DATASET_PATH = '/kaggle/input/binancebot-package'

# Chuyển vào folder dataset
os.chdir(DATASET_PATH)
print(f"Dataset path: {DATASET_PATH}")

# Chạy install script
print("\nRunning installation...")
result = subprocess.run(['bash', 'install.sh'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)

# Verify installation
result = subprocess.run(['binancebot', '--version'], capture_output=True, text=True)
if result.returncode == 0:
    print(f"\n✅ BinanceBot installed: {result.stdout.strip()}")
else:
    print("\n❌ Installation failed!")
    print(result.stderr)

# Quay lại working directory
os.chdir('/kaggle/working')
print("✅ Ready to start!")


# ===== CELL 2: Import Libraries =====
import json
import shutil
from pathlib import Path
from datetime import datetime

print("✅ Libraries imported")


# ===== CELL 3: Configuration =====
CONFIG = {
    'strategy': 'UniversalMACD',
    'timeframes': ['4h', '12h', '1d'],
    'pairs': ['BTC/USDT', 'ETH/USDT', 'BNB/USDT'],
    'epochs': 100,
    'loss_function': 'SharpeHyperOptLoss',
    'hyperopt_timerange': '20200101-20231231',  # Train: 2020-2023 (4 years)
    'backtest_timerange': '20240101-20251031',  # Test: 2024-2025 (22 months)
}

# Paths
WORK_DIR = Path('/kaggle/working')
USER_DATA = WORK_DIR / 'user_data'
CONFIG_PATH = WORK_DIR / 'config.json'

print("Configuration:")
print(f"  Strategy: {CONFIG['strategy']}")
print(f"  Timeframes: {CONFIG['timeframes']}")
print(f"  Epochs: {CONFIG['epochs']}")
print(f"  Total runs: {len(CONFIG['timeframes'])}")


# ===== CELL 4: Create Config File =====
# Tạo config cho BinanceBot
config_data = {
    "max_open_trades": 3,
    "stake_currency": "USDT",
    "stake_amount": 30,
    "dry_run": True,
    "timeframe": "4h",
    "exchange": {
        "name": "binance",
        "pair_whitelist": CONFIG['pairs'],
        "pair_blacklist": []
    },
    "pairlists": [{"method": "StaticPairList"}]
}

CONFIG_PATH.write_text(json.dumps(config_data, indent=2))
print(f"✅ Config created: {CONFIG_PATH}")


# ===== CELL 5: Create Strategy File =====
# Copy strategy từ repo
strategy_code = '''
import numpy as np
import talib.abstract as ta
from pandas import DataFrame
from binancebot.strategy import IStrategy, IntParameter

class UniversalMACD(IStrategy):
    """
    Universal MACD Strategy với hyperoptable parameters
    """
    
    # ROI table
    minimal_roi = {
        "0": 0.10,
        "30": 0.05,
        "60": 0.02,
        "120": 0.01
    }
    
    stoploss = -0.10
    trailing_stop = False
    
    # Hyperoptable parameters
    buy_macd_fast = IntParameter(8, 16, default=12, space='buy')
    buy_macd_slow = IntParameter(20, 30, default=26, space='buy')
    
    sell_macd_fast = IntParameter(8, 16, default=12, space='sell')
    sell_macd_slow = IntParameter(20, 30, default=26, space='sell')
    
    timeframe = '4h'
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # MACD with buy parameters
        macd_buy = ta.MACD(dataframe, 
                          fastperiod=self.buy_macd_fast.value,
                          slowperiod=self.buy_macd_slow.value,
                          signalperiod=9)
        dataframe['macd_buy'] = macd_buy['macd']
        dataframe['macdsignal_buy'] = macd_buy['macdsignal']
        
        # MACD with sell parameters  
        macd_sell = ta.MACD(dataframe,
                           fastperiod=self.sell_macd_fast.value,
                           slowperiod=self.sell_macd_slow.value,
                           signalperiod=9)
        dataframe['macd_sell'] = macd_sell['macd']
        dataframe['macdsignal_sell'] = macd_sell['macdsignal']
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['macd_buy'] > dataframe['macdsignal_buy']),
            'enter_long'] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['macd_sell'] < dataframe['macdsignal_sell']),
            'exit_long'] = 1
        return dataframe
'''

# Tạo strategy folder
strategy_dir = USER_DATA / 'strategies'
strategy_dir.mkdir(parents=True, exist_ok=True)
strategy_file = strategy_dir / 'UniversalMACD.py'
strategy_file.write_text(strategy_code)

print(f"✅ Strategy created: {strategy_file}")


# ===== CELL 6: Download Data =====
def download_data(timeframe):
    """Download dữ liệu lịch sử"""
    print(f"\n📥 Downloading {timeframe} data...")
    
    cmd = [
        'binancebot', 'download-data',
        '--pairs', *CONFIG['pairs'],
        '--timeframe', timeframe,
        '--timerange', CONFIG['hyperopt_timerange'],
        '--config', str(CONFIG_PATH),
        '--userdir', str(USER_DATA)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {timeframe} downloaded")
    else:
        print(f"❌ Error downloading {timeframe}")
        print(result.stderr[-500:])

# Download tất cả timeframes
for tf in CONFIG['timeframes']:
    download_data(tf)


# ===== CELL 7: Run Hyperopt & Backtest =====
def run_hyperopt(timeframe):
    """Chạy hyperopt cho 1 timeframe"""
    print(f"\n{'='*70}")
    print(f"HYPEROPT: {CONFIG['strategy']} @ {timeframe}")
    print(f"   Epochs: {CONFIG['epochs']} | Loss: {CONFIG['loss_function']}")
    print(f"{'='*70}")
    
    cmd = [
        'binancebot', 'hyperopt',
        '--strategy', CONFIG['strategy'],
        '--timeframe', timeframe,
        '--timerange', CONFIG['hyperopt_timerange'],
        '--epochs', str(CONFIG['epochs']),
        '--hyperopt-loss', CONFIG['loss_function'],
        '--config', str(CONFIG_PATH),
        '--userdir', str(USER_DATA),
        '--spaces', 'buy', 'sell', 'roi', 'stoploss',
    ]
    
    # Chạy và theo dõi
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    epoch = 0
    for line in process.stdout:
        # Print progress
        if 'Best result:' in line:
            print(line.rstrip())
        elif 'epoch' in line.lower() and '/' in line:
            epoch += 1
            if epoch % 10 == 0:  # Print mỗi 10 epochs
                print(f"   Progress: {epoch}/{CONFIG['epochs']} epochs...")
        elif 'Objective:' in line:
            print(line.rstrip())
    
    process.wait()
    
    if process.returncode == 0:
        print(f"\nHyperopt COMPLETE: {timeframe}")
        return True
    else:
        print(f"\nHyperopt FAILED: {timeframe}")
        return False

def run_backtest(timeframe):
    """Chạy backtest cho 1 timeframe"""
    print(f"\n{'='*70}")
    print(f"BACKTEST: {CONFIG['strategy']} @ {timeframe}")
    print(f"   Timerange: {CONFIG['backtest_timerange']}")
    print(f"{'='*70}")
    
    cmd = [
        'binancebot', 'backtesting',
        '--strategy', CONFIG['strategy'],
        '--timeframe', timeframe,
        '--timerange', CONFIG['backtest_timerange'],
        '--config', str(CONFIG_PATH),
        '--userdir', str(USER_DATA)
    ]
    
    # Chạy và theo dõi
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    output_lines = []
    for line in process.stdout:
        output_lines.append(line)
        # Print important lines
        if any(keyword in line for keyword in [
            'BACKTESTING REPORT', 'Total/Daily', 'Win', 'Loss', 'Avg profit',
            'Total profit', 'Trades', 'Drawdown'
        ]):
            print(line.rstrip())
    
    process.wait()
    
    if process.returncode == 0:
        print(f"\nBacktest COMPLETE: {timeframe}")
        # Parse metrics
        metrics = parse_backtest_output(''.join(output_lines))
        return True, metrics
    else:
        print(f"\nBacktest FAILED: {timeframe}")
        return False, {}

def parse_backtest_output(output):
    """Parse backtest output to extract key metrics"""
    metrics = {}
    
    for line in output.split('\n'):
        if 'Total profit' in line or 'Absolute profit' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                metrics['total_profit'] = parts[1].strip()
        elif 'Total trades' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                metrics['trades'] = parts[1].strip()
        elif 'Win  Draw  Loss' in line:
            # Next line has the values
            continue
        elif 'Avg. Duration' in line or 'Avg Duration' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                metrics['avg_duration'] = parts[1].strip()
        elif 'Max Drawdown' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                metrics['max_drawdown'] = parts[1].strip()
    
    return metrics

# Chạy hyperopt + backtest cho tất cả timeframes
results = {}
all_metrics = []

for idx, tf in enumerate(CONFIG['timeframes'], 1):
    print(f"\n\n{'#'*70}")
    print(f"# COMBINATION {idx}/{len(CONFIG['timeframes'])}: {tf}")
    print(f"{'#'*70}")
    
    # Step 1: Hyperopt
    hyperopt_success = run_hyperopt(tf)
    
    # Step 2: Backtest (nếu hyperopt thành công)
    backtest_success = False
    metrics = {}
    
    if hyperopt_success:
        backtest_success, metrics = run_backtest(tf)
    
    # Store results
    results[tf] = {
        'hyperopt': 'SUCCESS' if hyperopt_success else 'FAILED',
        'backtest': 'SUCCESS' if backtest_success else 'FAILED',
        'metrics': metrics
    }
    
    # Store metrics for summary
    if backtest_success:
        all_metrics.append({
            'timeframe': tf,
            **metrics
        })
    
    # In summary sau mỗi run
    print(f"\n PROGRESS SUMMARY:")
    for timeframe, data in results.items():
        h_icon = 'OK' if data['hyperopt'] == 'SUCCESS' else 'FAIL'
        b_icon = 'OK' if data['backtest'] == 'SUCCESS' else 'FAIL'
        print(f"   {timeframe}: Hyperopt [{h_icon}] | Backtest [{b_icon}]")
        if data['metrics']:
            print(f"      Profit: {data['metrics'].get('total_profit', 'N/A')}")
            print(f"      Trades: {data['metrics'].get('trades', 'N/A')}")


# ===== CELL 8: Save Results =====
# Tạo output folder
output_dir = WORK_DIR / 'training_results'
output_dir.mkdir(exist_ok=True)

# Copy hyperopt results
hyperopt_dir = USER_DATA / 'hyperopt_results'
if hyperopt_dir.exists():
    for file in hyperopt_dir.glob('*.fthypt'):
        shutil.copy(file, output_dir)
        print(f"Saved: {file.name}")

# Copy optimized parameters
strategy_json = USER_DATA / 'strategies' / f'{CONFIG["strategy"]}.json'
if strategy_json.exists():
    shutil.copy(strategy_json, output_dir)
    print(f"Saved: {strategy_json.name}")

# Copy backtest results
backtest_dir = USER_DATA / 'backtest_results'
if backtest_dir.exists():
    for file in backtest_dir.glob('*.json'):
        shutil.copy(file, output_dir)
        print(f"Saved: {file.name}")

# Tạo comprehensive summary file
summary_file = output_dir / 'complete_summary.txt'
with open(summary_file, 'w', encoding='utf-8') as f:
    f.write(f"Complete Training & Backtest Summary\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"{'='*70}\n\n")
    f.write(f"Strategy: {CONFIG['strategy']}\n")
    f.write(f"Epochs: {CONFIG['epochs']}\n")
    f.write(f"Timeframes: {', '.join(CONFIG['timeframes'])}\n")
    f.write(f"Train Period: {CONFIG['hyperopt_timerange']}\n")
    f.write(f"Test Period: {CONFIG['backtest_timerange']}\n\n")
    
    f.write("="*70 + "\n")
    f.write("RESULTS BY TIMEFRAME\n")
    f.write("="*70 + "\n\n")
    
    for tf, data in results.items():
        f.write(f"\nTimeframe: {tf}\n")
        f.write(f"  Hyperopt: {data['hyperopt']}\n")
        f.write(f"  Backtest: {data['backtest']}\n")
        
        if data['metrics']:
            f.write(f"  Metrics:\n")
            for key, value in data['metrics'].items():
                f.write(f"    {key}: {value}\n")
        f.write("\n")
    
    # Best performing timeframe
    if all_metrics:
        f.write("="*70 + "\n")
        f.write("BEST PERFORMING TIMEFRAME\n")
        f.write("="*70 + "\n")
        # Simple heuristic: timeframe with most trades or mentioned profit
        f.write(f"Total timeframes tested: {len(all_metrics)}\n")
        for metric in all_metrics:
            f.write(f"\n{metric['timeframe']}:\n")
            for k, v in metric.items():
                if k != 'timeframe':
                    f.write(f"  {k}: {v}\n")

print(f"\nResults saved to: {output_dir}")

# Export metrics to CSV
if all_metrics:
    import csv
    csv_file = output_dir / 'backtest_metrics.csv'
    
    # Get all unique keys
    all_keys = set()
    for m in all_metrics:
        all_keys.update(m.keys())
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
        writer.writeheader()
        writer.writerows(all_metrics)
    
    print(f"Metrics CSV saved: {csv_file}")

print(f"\nDownload the 'training_results' folder from Output tab!")


# ===== CELL 9: Display Summary =====
print("\n" + "="*70)
print("TRAINING & BACKTEST COMPLETE!")
print("="*70)

print(f"\nStrategy: {CONFIG['strategy']}")
print(f"Epochs per timeframe: {CONFIG['epochs']}")
print(f"Total timeframes: {len(CONFIG['timeframes'])}")

print(f"\nRESULTS SUMMARY:")
print("-"*70)

for tf, data in results.items():
    h_status = 'SUCCESS' if data['hyperopt'] == 'SUCCESS' else 'FAILED'
    b_status = 'SUCCESS' if data['backtest'] == 'SUCCESS' else 'FAILED'
    
    print(f"\n{tf}:")
    print(f"  Hyperopt: {h_status}")
    print(f"  Backtest: {b_status}")
    
    if data['metrics']:
        print(f"  Metrics:")
        for key, value in data['metrics'].items():
            print(f"    - {key}: {value}")

print("\n" + "="*70)
print(f"Output folder: {output_dir}")
print("="*70)
print("\nDownload from Kaggle Output tab:")
print("  - *.fthypt files (hyperopt history)")
print("  - *.json files (backtest results + optimized params)")
print("  - complete_summary.txt (full summary)")
print("  - backtest_metrics.csv (metrics table)")
print("\nUse these files locally:")
print("  1. Copy *.fthypt to user_data/hyperopt_results/")
print("  2. Copy UniversalMACD.json to user_data/strategies/")
print("  3. Run backtest locally with optimized params")


# ===== CELL 10: AUTO RUN =====
# Uncomment dòng dưới để tự động chạy toàn bộ pipeline
# Hoặc comment lại nếu muốn chạy từng cell riêng

print("\n" + "="*70)
print("AUTO EXECUTION")
print("="*70)
print("Starting full pipeline in 3 seconds...")
print("Press Ctrl+C to cancel")

import time
time.sleep(3)

# Chạy pipeline tự động
print("\nExecuting cells 3-9...")
exec(compile(open(__file__).read(), __file__, 'exec'))
