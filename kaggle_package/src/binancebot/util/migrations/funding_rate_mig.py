import logging

from binancebot.constants import Config
from binancebot.enums import TradingMode
from binancebot.exchange import Exchange


logger = logging.getLogger(__name__)


def migrate_funding_fee_timeframe(config: Config, exchange: Exchange | None):
    from binancebot.data.history import get_datahandler

    if config.get("trading_mode", TradingMode.SPOT) != TradingMode.FUTURES:
        # only act on futures
        return

    if not exchange:
        from binancebot.resolvers import ExchangeResolver

        exchange = ExchangeResolver.load_exchange(config, validate=False)

    ff_timeframe = exchange.get_option("funding_fee_timeframe")

    dhc = get_datahandler(config["datadir"], config["dataformat_ohlcv"])
    dhc.fix_funding_fee_timeframe(ff_timeframe)
