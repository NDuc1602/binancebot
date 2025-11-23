# pragma pylint: disable=attribute-defined-outside-init

"""
This module load a custom model for AIML
"""

import logging
from pathlib import Path

from binancebot.constants import USERPATH_AIMLMODELS, Config
from binancebot.exceptions import OperationalException
from binancebot.aiml.AIML_interface import IAIMLModel
from binancebot.resolvers import IResolver


logger = logging.getLogger(__name__)


class AIMLModelResolver(IResolver):
    """
    This class contains all the logic to load custom hyperopt loss class
    """

    object_type = IAIMLModel
    object_type_str = "AIMLModel"
    user_subdir = USERPATH_AIMLMODELS
    initial_search_path = (
        Path(__file__).parent.parent.joinpath("AIML/prediction_models").resolve()
    )
    extra_path = "AIMLmodel_path"

    @staticmethod
    def load_AIMLmodel(config: Config) -> IAIMLModel:
        """
        Load the custom class from config parameter
        :param config: configuration dictionary
        """
        disallowed_models = ["BaseRegressionModel"]

        AIMLmodel_name = config.get("AIMLmodel")
        if not AIMLmodel_name:
            raise OperationalException(
                "No AIMLmodel set. Please use `--AIMLmodel` to "
                "specify the AIMLModel class to use.\n"
            )
        if AIMLmodel_name in disallowed_models:
            raise OperationalException(
                f"{AIMLmodel_name} is a baseclass and cannot be used directly. Please choose "
                "an existing child class or inherit from this baseclass.\n"
            )
        AIMLmodel = AIMLModelResolver.load_object(
            AIMLmodel_name,
            config,
            kwargs={"config": config},
        )

        return AIMLmodel
