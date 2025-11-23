"""
Prepare Data for Kaggle Upload
================================

This script helps you prepare the downloaded data for uploading to Kaggle.

Steps:
1. Run this script to create a zip file of your data
2. Upload the zip to Kaggle as a dataset
3. Add the dataset to your notebook
4. Extract data in the notebook

Usage:
    python prepare_kaggle_dataset.py
"""

import shutil
import json
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
USER_DATA = PROJECT_ROOT / 'user_data'
DATA_DIR = USER_DATA / 'data' / 'binance'
OUTPUT_DIR = PROJECT_ROOT / 'backtest' / 'kaggle_dataset'

def check_data_exists():
    """Check if data directory exists and has files"""
    print("="*70)
    print("🔍 CHECKING DATA AVAILABILITY")
    print("="*70)
    
    if not DATA_DIR.exists():
        print(f"\n❌ Data directory not found: {DATA_DIR}")
        print("\n💡 You need to download data first:")
        print("   binancebot download-data --pairs BTC/USDT ETH/USDT BNB/USDT \\")
        print("     --timeframes 4h 12h 1d \\")
        print("     --timerange 20200101-20251122 \\")
        print("     --config config/config_binance.example.json \\")
        print("     --userdir user_data")
        return False
    
    # List all data files (support both .json and .feather formats)
    json_files = list(DATA_DIR.glob('*.json'))
    feather_files = list(DATA_DIR.glob('*.feather'))
    data_files = json_files + feather_files
    
    if not data_files:
        print(f"\n❌ No data files found in: {DATA_DIR}")
        return False
    
    print(f"\n✓ Found {len(data_files)} data files:")
    print(f"   JSON: {len(json_files)}")
    print(f"   Feather: {len(feather_files)}")
    
    # Group by pair and timeframe
    by_pair = {}
    for file in data_files:
        name = file.stem  # e.g., BTC_USDT-4h
        if '-' in name:
            pair, tf = name.rsplit('-', 1)
            pair = pair.replace('_', '/')
            if pair not in by_pair:
                by_pair[pair] = []
            by_pair[pair].append(tf)
    
    for pair, timeframes in sorted(by_pair.items()):
        print(f"  {pair}: {', '.join(sorted(timeframes))}")
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in data_files)
    size_mb = total_size / (1024 * 1024)
    print(f"\n📊 Total size: {size_mb:.2f} MB")
    
    return True

def create_dataset():
    """Create Kaggle dataset structure"""
    print("\n" + "="*70)
    print("📦 CREATING KAGGLE DATASET")
    print("="*70)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create data directory in output
    dataset_data = OUTPUT_DIR / 'data' / 'binance'
    dataset_data.mkdir(parents=True, exist_ok=True)
    
    # Copy data files (both .json and .feather)
    json_files = list(DATA_DIR.glob('*.json'))
    feather_files = list(DATA_DIR.glob('*.feather'))
    data_files = json_files + feather_files
    
    print(f"\n📋 Copying {len(data_files)} files...")
    print(f"   JSON: {len(json_files)}, Feather: {len(feather_files)}")
    
    for file in data_files:
        dest = dataset_data / file.name
        shutil.copy2(file, dest)
        print(f"  ✓ {file.name}")
    
    # Create dataset metadata
    metadata = {
        "title": "BinanceBot Training Data 2020-2025",
        "id": "yourusername/binancebot-data-2020-2025",
        "licenses": [{"name": "CC0-1.0"}],
        "description": f"Historical OHLCV data for BinanceBot training\n\n"
                      f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                      f"Pairs: BTC/USDT, ETH/USDT, BNB/USDT\n"
                      f"Timeframes: 4h, 12h, 1d\n"
                      f"Period: 2020-01-01 to 2025-11-22\n"
                      f"Files: {len(data_files)}",
    }
    
    metadata_file = OUTPUT_DIR / 'dataset-metadata.json'
    metadata_file.write_text(json.dumps(metadata, indent=2))
    print(f"\n✓ Created metadata: {metadata_file.name}")
    
    # Create README
    readme = f"""# BinanceBot Training Data (2020-2025)

## Description
Historical OHLCV data for cryptocurrency trading bot training.

## Contents
- **Pairs**: BTC/USDT, ETH/USDT, BNB/USDT
- **Timeframes**: 4h, 12h, 1d
- **Period**: 2020-01-01 to 2025-11-22 (~6 years)
- **Files**: {len(data_files)} JSON files
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

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    readme_file = OUTPUT_DIR / 'README.md'
    readme_file.write_text(readme, encoding='utf-8')
    print(f"✓ Created README: {readme_file.name}")
    
    return OUTPUT_DIR

def create_zip():
    """Create zip file for easy upload"""
    print("\n" + "="*70)
    print("🗜️  CREATING ZIP FILE")
    print("="*70)
    
    zip_name = f"binancebot-data-{datetime.now().strftime('%Y%m%d')}"
    zip_path = PROJECT_ROOT / 'backtest' / zip_name
    
    print(f"\n📦 Creating: {zip_path}.zip")
    shutil.make_archive(str(zip_path), 'zip', OUTPUT_DIR)
    
    zip_file = Path(f"{zip_path}.zip")
    size_mb = zip_file.stat().st_size / (1024 * 1024)
    
    print(f"✓ Zip created: {size_mb:.2f} MB")
    
    return zip_file

def main():
    print("\n" + "="*70)
    print("📊 BINANCEBOT DATA PREPARATION FOR KAGGLE")
    print("="*70)
    
    # Step 1: Check data
    if not check_data_exists():
        print("\n❌ Cannot proceed without data!")
        return
    
    # Step 2: Create dataset structure
    dataset_dir = create_dataset()
    
    # Step 3: Create zip file
    zip_file = create_zip()
    
    # Final instructions
    print("\n" + "="*70)
    print("✅ PREPARATION COMPLETE!")
    print("="*70)
    
    print(f"\n📁 Dataset folder: {dataset_dir}")
    print(f"📦 Zip file: {zip_file}")
    
    print("\n" + "="*70)
    print("📤 NEXT STEPS - UPLOAD TO KAGGLE:")
    print("="*70)
    
    print("\n1️⃣  Go to https://www.kaggle.com/datasets")
    print("2️⃣  Click 'New Dataset'")
    print(f"3️⃣  Upload the zip file: {zip_file.name}")
    print("4️⃣  Title: 'BinanceBot Training Data 2020-2025'")
    print("5️⃣  Click 'Create'")
    
    print("\n" + "="*70)
    print("📓 IN YOUR KAGGLE NOTEBOOK:")
    print("="*70)
    
    print("""
1. Add dataset to notebook:
   - Click '+ Add Data' → 'Your Datasets'
   - Select your uploaded dataset

2. Replace Cell 6 in notebook with:

```python
# CELL 6: Load Data from Kaggle Dataset
import shutil

print("="*70)
print("📥 LOADING DATA FROM KAGGLE DATASET")
print("="*70)

# Path to uploaded dataset (adjust username/dataset-name)
dataset_path = Path('/kaggle/input/binancebot-data-2020-2025/data')
target_path = USER_DATA / 'data'

print(f"\\nSource: {dataset_path}")
print(f"Target: {target_path}")

# Copy data
target_path.mkdir(parents=True, exist_ok=True)
shutil.copytree(dataset_path, target_path, dirs_exist_ok=True)

# Verify
data_files = list((target_path / 'binance').glob('*.json'))
print(f"\\n✓ Copied {len(data_files)} data files:")

by_pair = {}
for file in data_files:
    name = file.stem
    if '-' in name:
        pair, tf = name.rsplit('-', 1)
        pair = pair.replace('_', '/')
        if pair not in by_pair:
            by_pair[pair] = []
        by_pair[pair].append(tf)

for pair, timeframes in sorted(by_pair.items()):
    print(f"  {pair}: {', '.join(sorted(timeframes))}")

print("\\n" + "="*70)
print("✅ DATA LOADED - READY FOR TRAINING!")
print("="*70)
```

3. Continue with Cell 7 (Hyperopt & Backtest)
""")
    
    print("\n" + "="*70)
    print("🎉 ALL DONE!")
    print("="*70)
    print("\n💡 TIP: Keep the zip file for future use!")

if __name__ == '__main__':
    main()
