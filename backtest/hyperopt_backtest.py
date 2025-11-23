#!/usr/bin/env python3
"""
BinanceBot Hyperopt + Backtest Script
Tự động tối ưu parameters với Hyperopt, sau đó backtest để tìm chiến lược tốt nhất
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import time


class HyperoptBacktestRunner:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.strategies = [
            "GodStra",
            "Supertrend",
            "MultiMa",
            "UniversalMACD",
            "TemplateStrategy"
        ]
        self.results = {}
        
    def check_config(self):
        """Kiểm tra config file tồn tại"""
        if not Path(self.config_path).exists():
            print(f"Config file không tồn tại: {self.config_path}")
            print("Tạo config từ example:")
            print("  copy config\\config_binance.example.json config.json")
            sys.exit(1)
        print(f"Config file: {self.config_path}")
        
    def download_data(self, pairs, timeframe="4h", timerange="20200101-20251031"):
        """Download dữ liệu từ Binance (2020-01-01 đến 2025-10-31)"""
        print(f"\nDownloading data for {pairs} @ {timeframe}...")
        cmd = [
            "binancebot", "download-data",
            "--exchange", "binance",
            "--pairs", *pairs,
            "--timeframe", timeframe,
            "--timerange", timerange,
            "--config", self.config_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("Download hoàn tất")
        except subprocess.CalledProcessError as e:
            print(f"Download thất bại: {e}")
            sys.exit(1)
            
    def run_hyperopt(self, strategy, epochs=100, spaces=None, timerange=None, loss="SharpeHyperOptLoss"):
        """Chạy Hyperopt để tối ưu parameters"""
        print(f"\nHyperopt: {strategy}")
        print(f"   Epochs: {epochs}")
        print(f"   Loss function: {loss}")
        
        if spaces is None:
            spaces = ["buy", "sell", "roi", "stoploss"]
            
        cmd = [
            "binancebot", "hyperopt",
            "--config", self.config_path,
            "--strategy", strategy,
            "--epochs", str(epochs),
            "--spaces", *spaces,
            "--hyperopt-loss", loss,
            "--random-state", "42",  # Reproducible results
        ]
        
        if timerange:
            cmd.extend(["--timerange", timerange])
            
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                check=True
            )
            elapsed = time.time() - start_time
            
            print(f"{strategy} hyperopt hoàn tất ({elapsed:.1f}s)")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            print(f"{strategy} hyperopt thất bại")
            print(f"   Error: {e.stderr[:200]}")
            return False, None
            
    def run_backtest(self, strategy, timerange, stake_amount=100):
        """Chạy backtest với parameters đã optimize"""
        print(f"\nBacktesting: {strategy} (với optimized params)")
        
        cmd = [
            "binancebot", "backtesting",
            "--config", self.config_path,
            "--strategy", strategy,
            "--timerange", timerange,
            "--stake-amount", str(stake_amount),
            "--export", "trades"
        ]
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                check=True
            )
            
            # Parse kết quả
            output = result.stdout
            metrics = self._parse_backtest_results(output)
            
            print(f"{strategy} backtest hoàn tất")
            if metrics:
                print(f"   Total Profit: {metrics.get('total_profit', 'N/A')}")
                print(f"   Win Rate: {metrics.get('win_rate', 'N/A')}")
                print(f"   Max Drawdown: {metrics.get('max_drawdown', 'N/A')}")
                
            return True, metrics
        except subprocess.CalledProcessError as e:
            print(f"{strategy} backtest thất bại")
            return False, None
            
    def _parse_backtest_results(self, output):
        """Parse backtest output để lấy metrics"""
        metrics = {}
        try:
            lines = output.split('\n')
            for line in lines:
                if 'Total profit' in line or 'Absolute profit' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        metrics['total_profit'] = parts[1].strip()
                elif 'Win  Draw  Loss' in line:
                    # Next line contains win rate
                    idx = lines.index(line)
                    if idx + 1 < len(lines):
                        stats = lines[idx + 1].strip().split()
                        if len(stats) >= 3:
                            total = sum(int(x) for x in stats[:3])
                            if total > 0:
                                win_rate = (int(stats[0]) / total) * 100
                                metrics['win_rate'] = f"{win_rate:.1f}%"
                elif 'Max Drawdown' in line or 'Drawdown' in line:
                    parts = line.split(':')
                    if len(parts) > 1:
                        metrics['max_drawdown'] = parts[1].strip()
        except Exception as e:
            print(f"Không thể parse metrics: {e}")
            
        return metrics
        
    def run_full_pipeline(self, strategy, hyperopt_epochs, hyperopt_timerange, 
                         backtest_timerange, stake_amount, loss_function):
        """Chạy full pipeline: Hyperopt -> Backtest"""
        print(f"\n{'='*70}")
        print(f"STRATEGY: {strategy}")
        print(f"{'='*70}")
        
        # Step 1: Hyperopt
        hyperopt_success, hyperopt_output = self.run_hyperopt(
            strategy, 
            epochs=hyperopt_epochs,
            timerange=hyperopt_timerange,
            loss=loss_function
        )
        
        if not hyperopt_success:
            print(f"Bỏ qua backtest do hyperopt thất bại")
            return False
            
        # Step 2: Backtest với optimized params
        backtest_success, metrics = self.run_backtest(
            strategy,
            backtest_timerange,
            stake_amount
        )
        
        if backtest_success:
            self.results[strategy] = {
                'hyperopt_success': True,
                'backtest_success': True,
                'metrics': metrics
            }
            return True
        else:
            self.results[strategy] = {
                'hyperopt_success': True,
                'backtest_success': False,
                'metrics': None
            }
            return False
            
    def run_all_strategies(self, hyperopt_epochs, hyperopt_timerange, 
                          backtest_timerange, stake_amount, loss_function):
        """Chạy pipeline cho tất cả strategies"""
        print(f"\n{'='*70}")
        print(f"HYPEROPT + BACKTEST TẤT CẢ STRATEGIES")
        print(f"Hyperopt epochs: {hyperopt_epochs}")
        print(f"Hyperopt timerange: {hyperopt_timerange}")
        print(f"Backtest timerange: {backtest_timerange}")
        print(f"Loss function: {loss_function}")
        print(f"Số strategies: {len(self.strategies)}")
        print(f"{'='*70}\n")
        
        total_start = time.time()
        
        for i, strategy in enumerate(self.strategies, 1):
            print(f"\n[{i}/{len(self.strategies)}] ", end="")
            self.run_full_pipeline(
                strategy,
                hyperopt_epochs,
                hyperopt_timerange,
                backtest_timerange,
                stake_amount,
                loss_function
            )
            
        total_elapsed = time.time() - total_start
        
        # Summary
        self._print_summary(total_elapsed)
        
    def _print_summary(self, total_time):
        """In ra tổng kết kết quả"""
        print(f"\n{'='*70}")
        print(f"TỔNG KẾT KẾT QUẢ")
        print(f"Tổng thời gian: {total_time/60:.1f} phút")
        print(f"{'='*70}\n")
        
        # Sắp xếp theo profit
        ranked = []
        for strategy, data in self.results.items():
            if data.get('backtest_success') and data.get('metrics'):
                profit_str = data['metrics'].get('total_profit', '0%')
                try:
                    # Extract number from "X.XX%" or "X.XX USDT"
                    profit_val = float(profit_str.replace('%', '').replace('USDT', '').split()[0])
                except:
                    profit_val = 0
                    
                ranked.append({
                    'strategy': strategy,
                    'profit': profit_val,
                    'metrics': data['metrics']
                })
                
        ranked.sort(key=lambda x: x['profit'], reverse=True)
        
        # Top 5 strategies
        print("TOP 5 STRATEGIES TỐT NHẤT:\n")
        for i, item in enumerate(ranked[:5], 1):
            strategy = item['strategy']
            metrics = item['metrics']
            print(f"{i}. {strategy:20} | Profit: {metrics.get('total_profit', 'N/A'):15} | "
                  f"Win Rate: {metrics.get('win_rate', 'N/A'):8} | "
                  f"Drawdown: {metrics.get('max_drawdown', 'N/A')}")
                  
        # Failed strategies
        failed = [s for s, d in self.results.items() 
                 if not d.get('hyperopt_success') or not d.get('backtest_success')]
        if failed:
            print(f"\nSTRATEGIES THẤT BẠI: {', '.join(failed)}")
            
        print(f"\n{'='*70}")
        
    def save_results(self, output_file="hyperopt_backtest_results.json"):
        """Lưu kết quả ra file JSON"""
        output_path = Path("user_data") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print(f"\nKết quả đã lưu: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="BinanceBot Hyperopt + Backtest Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download data và chạy full pipeline
  python hyperopt_backtest.py --download --pairs BTC/USDT ETH/USDT --epochs 100
  
  # Chạy với loss function tùy chỉnh
  python hyperopt_backtest.py --loss SharpeHyperOptLossDaily --epochs 200
  
  # Chỉ chạy 1 strategy
  python hyperopt_backtest.py --strategy GodStra --epochs 50
  
  # Split train/test periods
  python hyperopt_backtest.py --hyperopt-timerange 20240101-20240630 --backtest-timerange 20240701-20241122
        """
    )
    
    parser.add_argument("--config", default="config.json", help="Config file")
    parser.add_argument("--download", action="store_true", help="Download data trước")
    parser.add_argument("--pairs", nargs="+", default=["BTC/USDT", "ETH/USDT", "BNB/USDT"], help="Trading pairs")
    parser.add_argument("--timeframe", default="4h", choices=["4h", "12h", "1d"], help="Timeframe (4h/12h/1d)")
    parser.add_argument("--data-timerange", default="20200101-20251031", help="Data download range (default: 2020-2025)")
    
    parser.add_argument("--epochs", type=int, default=100, help="Hyperopt epochs (default: 100)")
    parser.add_argument("--loss", default="SharpeHyperOptLoss", 
                       help="Loss function (default: SharpeHyperOptLoss)")
    
    parser.add_argument("--hyperopt-timerange", help="Timerange for hyperopt (training, default: 2020-2023)")
    parser.add_argument("--backtest-timerange", help="Timerange for backtest (testing, default: 2024-2025)")
    
    parser.add_argument("--stake-amount", type=float, default=100, help="Stake amount")
    parser.add_argument("--strategy", help="Run only specific strategy")
    parser.add_argument("--save-results", action="store_true", help="Save results to JSON")
    
    args = parser.parse_args()
    
    # Auto generate timeranges
    if not args.hyperopt_timerange:
        # Train: 2020-01-01 to 2023-12-31 (4 years)
        args.hyperopt_timerange = "20200101-20231231"
        
    if not args.backtest_timerange:
        # Test: 2024-01-01 to 2025-10-31 (22 months)
        args.backtest_timerange = "20240101-20251031"
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║          BINANCEBOT HYPEROPT + BACKTEST PIPELINE                  ║
╚═══════════════════════════════════════════════════════════════════╝

Configuration:
   • Pairs: {', '.join(args.pairs)}
   • Timeframe: {args.timeframe}
   • Hyperopt epochs: {args.epochs}
   • Loss function: {args.loss}
   • Train period: {args.hyperopt_timerange} (4 years)
   • Test period: {args.backtest_timerange} (22 months)
   • Stake amount: {args.stake_amount} USDT
""")
    
    # Initialize runner
    runner = HyperoptBacktestRunner(args.config)
    runner.check_config()
    
    # Download data
    if args.download:
        runner.download_data(args.pairs, args.timeframe, args.data_timerange)
    
    # Run pipeline
    if args.strategy:
        # Single strategy
        runner.strategies = [args.strategy]
        
    runner.run_all_strategies(
        hyperopt_epochs=args.epochs,
        hyperopt_timerange=args.hyperopt_timerange,
        backtest_timerange=args.backtest_timerange,
        stake_amount=args.stake_amount,
        loss_function=args.loss
    )
    
    # Save results
    if args.save_results:
        runner.save_results()
    
    print("\nPipeline hoàn tất!")
    print("Kết quả chi tiết: user_data/hyperopt_results/ và user_data/backtest_results/")


if __name__ == "__main__":
    main()
