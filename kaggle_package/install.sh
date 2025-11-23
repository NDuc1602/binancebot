#!/bin/bash
# Kaggle Installation Script

echo "Installing BinanceBot dependencies..."

# Install base requirements
pip install -q -r requirements/base.txt

# Install hyperopt requirements  
pip install -q -r requirements/hyperopt.txt

# Install BinanceBot
pip install -q -e .

echo "BinanceBot installed successfully!"
