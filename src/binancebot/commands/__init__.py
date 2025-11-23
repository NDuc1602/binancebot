# flake8: noqa: F401
"""
Commands module.
Contains all start-commands, subcommands and CLI Interface creation.

Note: Be careful with file-scoped imports in these subfiles.
    as they are parsed on startup, nothing containing optional modules should be loaded.
"""

from binancebot.commands.analyze_commands import start_analysis_entries_exits
from binancebot.commands.arguments import Arguments
from binancebot.commands.build_config_commands import start_new_config, start_show_config
from binancebot.commands.data_commands import (
    start_convert_data,
    start_convert_trades,
    start_download_data,
    start_list_data,
    start_list_trades_data,
)
from binancebot.commands.db_commands import start_convert_db
from binancebot.commands.deploy_commands import (
    start_create_userdir,
    start_install_ui,
    start_new_strategy,
)
from binancebot.commands.hyperopt_commands import start_hyperopt_list, start_hyperopt_show
from binancebot.commands.list_commands import (
    start_list_exchanges,
    start_list_AIML_models,
    start_list_hyperopt_loss_functions,
    start_list_markets,
    start_list_strategies,
    start_list_timeframes,
    start_show_trades,
)
from binancebot.commands.optimize_commands import (
    start_backtesting,
    start_backtesting_show,
    start_edge,
    start_hyperopt,
    start_lookahead_analysis,
    start_recursive_analysis,
)
from binancebot.commands.pairlist_commands import start_test_pairlist
from binancebot.commands.plot_commands import start_plot_dataframe, start_plot_profit
from binancebot.commands.strategy_utils_commands import start_strategy_update
from binancebot.commands.trade_commands import start_trading
from binancebot.commands.webserver_commands import start_webserver
