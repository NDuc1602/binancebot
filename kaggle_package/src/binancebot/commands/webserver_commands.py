from typing import Any

from binancebot.enums import RunMode


def start_webserver(args: dict[str, Any]) -> None:
    """
    Main entry point for webserver mode
    """
    from binancebot.configuration import setup_utils_configuration
    from binancebot.rpc.api_server import ApiServer

    # Initialize configuration

    config = setup_utils_configuration(args, RunMode.WEBSERVER)
    ApiServer(config, standalone=True)
