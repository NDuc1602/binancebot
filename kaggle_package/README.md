# BinanceBot - Crypto Trading Bot

**Đề tài:** Xây dựng Bot Giao dịch Tiền điện tử trên Binance Testnet

**Môn học:** Công nghệ Phần mềm (SE2025)  
**Nhóm:** 9.4

---

## 📖 Giới thiệu

BinanceBot là hệ thống trading bot tự động cho phép giao dịch tiền điện tử trên Binance. Bot hỗ trợ backtesting, paper trading (dry-run), và live trading với nhiều chiến lược đa dạng.

### ✨ Tính năng chính

- ✅ **Live Trading & Paper Trading** - Giao dịch thật hoặc giả lập
- ✅ **Backtesting** - Test chiến lược với dữ liệu lịch sử  
- ✅ **Hyperopt** - Tối ưu tham số tự động
- ✅ **25+ Trading Strategies** - Từ đơn giản đến phức tạp
- ✅ **Risk Management** - Stoploss, Trailing Stop, ROI, Protections
- ✅ **REST API** - Kết nối với Frontend
- ✅ **FreqAI** - Machine Learning cho trading
- ✅ **Binance Support** - Hỗ trợ Spot Trading

---

## 🏗️ Cấu trúc Project

```
SE2025-9.4/
├── .github/                # GitHub workflows (CI/CD)
│   └── workflows/
│
├── src/                    # Source code chính
│   └── binancebot/         # Core trading engine
│       ├── commands/       # CLI commands
│       ├── configuration/  # Config management
│       ├── data/           # Data handling
│       ├── exchange/       # Exchange connectors
│       ├── freqai/         # ML/AI features
│       ├── optimize/       # Backtesting & Hyperopt
│       ├── persistence/    # Database models
│       ├── plugins/        # Plugin system
│       ├── resolvers/      # Strategy/Exchange resolvers
│       ├── rpc/            # API & RPC
│       ├── strategy/       # Strategy framework
│       └── util/           # Utilities
│
├── strategies/             # Trading strategies (25)
│   └── user_data/
│       ├── strategies/     # Strategy files
│       └── hyperopts/      # Hyperopt configs
│
├── config/                 # Configuration examples
│   ├── config_binance.example.json
│   └── config_full.example.json
│
├── user_data/              # User data & models
│   ├── data/               # Downloaded market data
│   ├── strategies/         # Custom strategies
│   ├── freqaimodels/       # AI models
│   └── notebooks/          # Jupyter notebooks
│
├── scripts/                # Utility scripts
│   └── data_download/      # Data download tools
│       ├── download.js
│       └── *.csv
│
├── requirements/           # Dependencies
│   ├── base.txt           # Core dependencies
│   ├── hyperopt.txt       # Hyperopt extras
│   ├── plot.txt           # Plotting tools
│   ├── freqai.txt         # ML dependencies
│   ├── freqai_rl.txt      # Reinforcement Learning
│   └── dev.txt            # Development tools
│
├── tests/                  # Unit tests
├── docs/                   # Documentation
│
├── pyproject.toml         # Project configuration
├── README.md              # This file
└── LICENSE                # GPLv3 License
```

---

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống

- **Python:** >= 3.11
- **Node.js:** >= 18.x (cho data download)
- **TA-Lib:** Technical Analysis Library
- **PostgreSQL/SQLite:** Database

### Cài đặt dependencies

```bash
# Clone repository
git clone https://github.com/dangdoday/SE2025-9.4.git
cd SE2025-9.4

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt base dependencies
pip install -r requirements/base.txt

# Cài đặt extras (optional)
pip install -r requirements/hyperopt.txt  # Hyperopt
pip install -r requirements/plot.txt      # Plotting
pip install -r requirements/freqai.txt    # Machine Learning
pip install -r requirements/dev.txt       # Development
```

### Cài đặt TA-Lib

**Windows:**
```bash
pip install TA-Lib
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install ta-lib

# MacOS
brew install ta-lib

# Install Python wrapper
pip install TA-Lib
```

---

## ⚙️ Cấu hình

### Tạo config file

```bash
# Copy config mẫu
cp config/config_binance.example.json config.json

# Chỉnh sửa config
nano config.json
```

### Config cơ bản

```json
{
  "max_open_trades": 3,
  "stake_currency": "USDT",
  "stake_amount": 30,
  "dry_run": true,
  "exchange": {
    "name": "binance",
    "key": "your-api-key",
    "secret": "your-api-secret",
    "ccxt_config": {
      "enableRateLimit": true
    }
  }
}
```

---

## 📊 Sử dụng

### Download dữ liệu

```bash
# Sử dụng Node.js script
cd scripts/data_download
npm install
node download.js

# Hoặc sử dụng BinanceBot CLI
binancebot download-data --exchange binance --pairs BTC/USDT ETH/USDT --timeframe 1h --days 365
```

### Backtesting

```bash
binancebot backtesting \
  --config config.json \
  --strategy SampleStrategy \
  --timerange 20230101-20231231
```

### Hyperopt (Tối ưu tham số)

```bash
binancebot hyperopt \
  --config config.json \
  --strategy SampleStrategy \
  --epochs 100 \
  --spaces buy sell roi stoploss
```

### Paper Trading (Dry-run)

```bash
binancebot trade \
  --config config.json \
  --strategy SampleStrategy \
  --dry-run
```

### Live Trading

```bash
# ⚠️ Cẩn thận! Giao dịch thật với tiền thật
binancebot trade \
  --config config.json \
  --strategy SampleStrategy
```

---

## 📈 Strategies

Project bao gồm **25 strategies** được tối ưu:

### Basic Strategies (5)
- Strategy001-005: RSI, MACD, Bollinger Bands basics

### Advanced Strategies (10)
- GodStra, Supertrend, UniversalMACD, etc.

### Optimized Strategies (10)
- BinHV45, ClucMay72018, Discord strategies

Xem chi tiết tại: [`strategies/user_data/strategies/`](strategies/user_data/strategies/)

---

## 🔌 API Server

Start REST API:

```bash
binancebot webserver --config config.json
```

API sẽ chạy tại: `http://localhost:8080`

Swagger UI: `http://localhost:8080/docs`

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=binancebot tests/

# Run specific test
pytest tests/test_exchange.py
```

---

## 📚 Documentation

- **User Guide:** [`docs/`](docs/)
- **Strategy Development:** [`docs/strategies.md`](docs/strategies.md)
- **API Reference:** [`docs/api.md`](docs/api.md)
- **Configuration:** [`docs/configuration.md`](docs/configuration.md)

---

## 🤝 Đóng góp

Nhóm phát triển SE2025-9.4:
- Member 1
- Member 2
- Member 3

---

## 📄 License

GNU General Public License v3.0 - Xem [LICENSE](LICENSE)

---

## 🙏 Credits

Dựa trên [Freqtrade](https://github.com/freqtrade/freqtrade) - Open source crypto trading bot

---

## ⚠️ Disclaimer

Trading tiền điện tử có rủi ro cao. Sử dụng bot này hoàn toàn là trách nhiệm của bạn. Nhóm phát triển không chịu trách nhiệm về bất kỳ tổn thất tài chính nào.

**Khuyến nghị:**
- Test kỹ trên Testnet trước
- Bắt đầu với số vốn nhỏ
- Luôn sử dụng stop-loss
- Không bao giờ trade với tiền không thể mất
