"""
Chuẩn bị files để upload lên Kaggle Dataset
Tạo package có thể cài offline trên Kaggle
"""

import shutil
import subprocess
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
KAGGLE_PACKAGE = PROJECT_ROOT / 'kaggle_package'

print("Chuẩn bị Kaggle package...")
print(f"Project root: {PROJECT_ROOT}")

# Xóa folder cũ nếu có
if KAGGLE_PACKAGE.exists():
    shutil.rmtree(KAGGLE_PACKAGE)
    print("✓ Đã xóa package cũ")

# Tạo folder mới
KAGGLE_PACKAGE.mkdir()
print(f"✓ Tạo folder: {KAGGLE_PACKAGE}")

# 1. Copy source code
print("\n1. Copying source code...")
src_dir = KAGGLE_PACKAGE / 'src'
shutil.copytree(PROJECT_ROOT / 'src', src_dir)
print(f"   ✓ Copied: src/")

# 2. Copy requirements
print("\n2. Copying requirements...")
req_dir = KAGGLE_PACKAGE / 'requirements'
shutil.copytree(PROJECT_ROOT / 'requirements', req_dir)
print(f"   ✓ Copied: requirements/")

# 3. Copy setup files
print("\n3. Copying setup files...")
for file in ['setup.py', 'pyproject.toml', 'README.md']:
    src_file = PROJECT_ROOT / file
    if src_file.exists():
        shutil.copy(src_file, KAGGLE_PACKAGE / file)
        print(f"   ✓ Copied: {file}")

# 4. Copy strategy
print("\n4. Copying UniversalMACD strategy...")
strategy_src = PROJECT_ROOT / 'user_data' / 'strategies' / 'UniversalMACD.py'
strategy_dest = KAGGLE_PACKAGE / 'UniversalMACD.py'
if strategy_src.exists():
    shutil.copy(strategy_src, strategy_dest)
    print(f"   ✓ Copied: UniversalMACD.py")

# 5. Copy config example
print("\n5. Copying config...")
config_src = PROJECT_ROOT / 'config' / 'config_binance.example.json'
config_dest = KAGGLE_PACKAGE / 'config_binance.json'
if config_src.exists():
    shutil.copy(config_src, config_dest)
    print(f"   ✓ Copied: config_binance.json")

# 6. Tạo install script cho Kaggle
print("\n6. Creating install script...")
install_script = """#!/bin/bash
# Kaggle Installation Script

echo "Installing BinanceBot dependencies..."

# Install base requirements
pip install -q -r requirements/base.txt

# Install hyperopt requirements  
pip install -q -r requirements/hyperopt.txt

# Install BinanceBot
pip install -q -e .

echo "BinanceBot installed successfully!"
"""

# Write with Unix line endings (LF)
(KAGGLE_PACKAGE / 'install.sh').write_text(install_script, encoding='utf-8', newline='\n')
print("   ✓ Created: install.sh")

# 7. Tạo README cho Kaggle
print("\n7. Creating Kaggle README...")
readme_content = """# BinanceBot Kaggle Package

## Cai dat tren Kaggle

```python
# Cell 1: Install
import os
os.chdir('/kaggle/input/binancebot-package')
!bash install.sh
```

## Files included

- `src/` - BinanceBot source code
- `requirements/` - Dependencies
- `setup.py` - Installation script
- `UniversalMACD.py` - Trading strategy
- `config_binance.json` - Configuration
- `install.sh` - Auto install script

## Usage

Sau khi cai dat, su dung:
```python
!binancebot --version
```

Upload folder nay len Kaggle Dataset de su dung.
"""

# Write with Unix line endings (LF)
(KAGGLE_PACKAGE / 'KAGGLE_README.md').write_text(readme_content, encoding='utf-8', newline='\n')
print("   ✓ Created: KAGGLE_README.md")

# 8. Tạo ZIP file
print("\n8. Creating ZIP archive...")
zip_file = PROJECT_ROOT / 'binancebot_kaggle_package'
shutil.make_archive(zip_file, 'zip', KAGGLE_PACKAGE)
print(f"   ✓ Created: {zip_file}.zip")

print("\n" + "="*70)
print("KAGGLE PACKAGE READY!")
print("="*70)
print(f"\nPackage location: {KAGGLE_PACKAGE}")
print(f"ZIP file: {zip_file}.zip")
print("\nNext steps:")
print("1. Upload 'kaggle_package' folder to Kaggle Dataset")
print("   hoac upload 'binancebot_kaggle_package.zip'")
print("2. Trong Kaggle Notebook, Add Dataset nay")
print("3. Chay: !bash /kaggle/input/<dataset-name>/install.sh")
print("4. Chay kaggle_train.py")
