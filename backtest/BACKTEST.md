# Backtesting & Hyperopt Guide

Scripts và Jupyter Notebook để optimize và backtest strategies trên nhiều khung thời gian.

## 📂 Files

1. **`hyperopt_backtest.py`** - Hyperopt + Backtest pipeline (Command-line)
2. **`backtest_notebook.ipynb`** - Jupyter Notebook với multi-timeframe support ⭐
3. **`BACKTEST.md`** - Tài liệu này

## 📊 Strategies Available (7)

- BasicRSI
- BasicADX
- GodStra
- Supertrend
- MultiMa
- UniversalMACD
- TemplateStrategy

## ⏰ Timeframes & Data Period

- **Timeframes**: `4h`, `12h`, `1d` (3 khung thời gian chính)
- **Data Period**: 2020-01-01 đến 2025-10-31 (5 năm 10 tháng)
- **Train Period**: 2020-01-01 đến 2023-12-31 (4 năm)
- **Test Period**: 2024-01-01 đến 2025-10-31 (22 tháng)

## Cài đặt

```bash
# Activate virtual environment
venv\Scripts\activate

# Cài đặt BinanceBot
pip install -e .

# Cài thêm dependencies cho notebook (nếu dùng Jupyter)
pip install jupyter matplotlib pandas
```

---

## 🚀 JUPYTER NOTEBOOK (Multi-Timeframe) ⭐

**File:** `backtest_notebook.ipynb`

### Features

✅ **Multi-Timeframe Support** - Test trên 4h, 12h, 1d cùng lúc  
✅ **Long-term Data** - 5+ years của data (2020-2025)
✅ **Visual Results** - Biểu đồ so sánh chi tiết  
✅ **Persistent Storage** - Lưu kết quả trong notebook  
✅ **Export** - CSV, JSON, Markdown  
✅ **Flexible** - Chạy từng bước hoặc full pipeline  

### Quick Start

```python
# 1. Open notebook
jupyter notebook backtest_notebook.ipynb

# 2. Run all cells hoặc:
run_full_pipeline()  # Chạy tất cả strategies trên tất cả timeframes

# 3. Customize
run_full_pipeline(
    strategies=['BasicRSI', 'GodStra'],
    timeframes=['4h', '1d']
)
```

### Results

- **By Timeframe**: Top strategies cho mỗi khung thời gian (4h/12h/1d)
- **Overall Ranking**: Top 10 best combinations
- **Visualizations**: Profit, Win Rate, Drawdown charts
- **Export**: Auto export to `results/` folder

---

## 🎯 HYPEROPT + BACKTEST (Python Script)

Tự động tìm parameters tốt nhất, sau đó test trên data riêng biệt.

### Quick Start

```bash
# Download data và chạy full pipeline (timeframe 4h)
python hyperopt_backtest.py --download --timeframe 4h --epochs 100

# Với timeframe khác
python hyperopt_backtest.py --download --timeframe 12h --epochs 200
python hyperopt_backtest.py --download --timeframe 1d --epochs 100
```

### Pipeline Flow

```
1. Download Data (2020-2025, 5+ years)
   ↓
2. Split data:
   • Train: 2020-2023 (4 years) - cho Hyperopt
   • Test: 2024-2025 (22 months) - cho Backtest
   ↓
3. Hyperopt (tìm best params trên train data)
   ↓
4. Backtest (test với best params trên test data)
   ↓
5. Rank strategies theo performance
```

### Examples

```bash
# 1. Chạy tất cả 7 strategies với timeframe 4h
python hyperopt_backtest.py --download --timeframe 4h --epochs 100

# 2. Timeframe 12h với loss function khác
python hyperopt_backtest.py --timeframe 12h --loss SharpeHyperOptLossDaily --epochs 200

# 3. Chỉ test 1 strategy trên timeframe 1d
python hyperopt_backtest.py --strategy GodStra --timeframe 1d --epochs 50

# 4. Custom train/test split
python hyperopt_backtest.py ^
  --timeframe 4h ^
  --hyperopt-timerange 20200101-20221231 ^
  --backtest-timerange 20230101-20251031 ^
  --epochs 100

# 5. Full options
python hyperopt_backtest.py ^
  --download ^
  --pairs BTC/USDT ETH/USDT BNB/USDT ^
  --timeframe 4h ^
  --epochs 200 ^
  --loss SharpeHyperOptLossDaily ^
  --stake-amount 100 ^
  --save-results
```

### Kết quả

Script sẽ hiển thị:
- ✅ Progress mỗi strategy
- 📊 Metrics: Total Profit, Win Rate, Max Drawdown
- 🏆 **Top 5 strategies tốt nhất**
- 💾 Lưu kết quả JSON (nếu `--save-results`)

---

## 📊 CLI COMMANDS

### Download Data

```bash
# Download cho timeframe 4h
binancebot download-data ^
  --pairs BTC/USDT ETH/USDT BNB/USDT ^
  --timeframe 4h ^
  --timerange 20200101-20251031

# Download cho timeframe 12h
binancebot download-data ^
  --pairs BTC/USDT ETH/USDT BNB/USDT ^
  --timeframe 12h ^
  --timerange 20200101-20251031

# Download cho timeframe 1d
binancebot download-data ^
  --pairs BTC/USDT ETH/USDT BNB/USDT ^
  --timeframe 1d ^
  --timerange 20200101-20251031
```

### Backtest đơn giản

```bash
# Backtest với strategy cụ thể
binancebot backtesting ^
  --strategy BasicRSI ^
  --timeframe 4h ^
  --timerange 20240101-20251031

# Backtest với config file
binancebot backtesting ^
  --config config/config_binance.example.json ^
  --strategy GodStra ^
  --timeframe 12h ^
  --timerange 20240101-20251031
```

### Hyperopt

```bash
# Optimize parameters
binancebot hyperopt ^
  --strategy Supertrend ^
  --timeframe 4h ^
  --timerange 20200101-20231231 ^
  --epochs 100 ^
  --spaces buy sell roi stoploss

# Với loss function khác
binancebot hyperopt ^
  --strategy MultiMa ^
  --timeframe 1d ^
  --timerange 20200101-20231231 ^
  --epochs 200 ^
  --hyperopt-loss SharpeHyperOptLossDaily
```

## Kết quả

Kết quả backtest được lưu tại:
- `user_data/backtest_results/` - JSON results
- `user_data/hyperopt_results/` - Hyperopt results
- `backtest/results/` - Notebook export (CSV/JSON/Markdown)

## Xem kết quả

```bash
# Xem kết quả backtest
binancebot backtesting-show

# Xem trade list
binancebot backtesting-show --show-trades

# Xem hyperopt results
binancebot hyperopt-show
```

# Export sang CSV
binancebot backtesting-show --export-csv
```

## Strategies được test

1. BasicRSI - RSI + Bollinger Bands
2. BasicADX - ADX + RSI
3. GodStra - Multi-indicator
4. Supertrend - Trend following
5. MultiMa - Multiple MA
6. UniversalMACD - MACD optimized
7. TemplateStrategy - Template
8. HighPerformance - Optimized
9. OptimizedCluc - Proven winner
10. HybridStrategy - Combined
11. ScalpingStrategy - Scalping

---

## 🎓 Loss Functions

Hyperopt hỗ trợ nhiều loss functions:

- **SharpeHyperOptLoss** - Sharpe Ratio (default)
- **SharpeHyperOptLossDaily** - Daily Sharpe Ratio
- **SortinoHyperOptLoss** - Sortino Ratio
- **SortinoHyperOptLossDaily** - Daily Sortino Ratio
- **MaxDrawDownHyperOptLoss** - Minimize drawdown
- **CalmarHyperOptLoss** - Calmar Ratio
- **ProfitDrawDownHyperOptLoss** - Profit/Drawdown balance

Example:
```bash
python hyperopt_backtest.py --loss SortinoHyperOptLossDaily --epochs 150
```

---

## 📈 So sánh kết quả

Sau khi chạy, xem kết quả chi tiết:

```bash
# Xem tất cả kết quả backtest
binancebot backtesting-show

# Xem hyperopt results
binancebot hyperopt-show

# Xem best params
binancebot hyperopt-show --best

# Export results
binancebot hyperopt-show --print-json > results.json
```

---

## ⚡ Tips

1. **Epochs**: 
   - 50-100 epochs: Quick test
   - 200-500 epochs: Serious optimization
   - 1000+ epochs: Deep search (slow)

2. **Train/Test Split**:
   - Train: 6-12 tháng
   - Test: 3-6 tháng riêng biệt
   - Tránh overfitting

3. **Loss Function**:
   - SharpeHyperOptLoss: Balanced
   - MaxDrawDownHyperOptLoss: Low risk
   - ProfitDrawDownHyperOptLoss: Aggressive

4. **Multiple Pairs**:
   - Test trên nhiều pairs để tránh overfitting
   - BTC/USDT, ETH/USDT, BNB/USDT recommended
