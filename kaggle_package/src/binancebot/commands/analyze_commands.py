import logging
from typing import Any

from binancebot.enums import RunMode


logger = logging.getLogger(__name__)


def start_analysis_entries_exits(args: dict[str, Any]) -> None:
    """
    Start analysis script
    :param args: Cli args from Arguments()
    :return: None
    """
    from binancebot.configuration import setup_utils_configuration
    from binancebot.data.entryexitanalysis import process_entry_exit_reasons

    # Initialize configuration
    config = setup_utils_configuration(args, RunMode.UTIL_NO_EXCHANGE)

    logger.info("Starting binancebot in analysis mode")

    process_entry_exit_reasons(config)
