# ensure users can still use a non-torch AIML version
try:
    from binancebot.aiml.tensorboard.tensorboard import TensorBoardCallback, TensorboardLogger

    TBLogger = TensorboardLogger
    TBCallback = TensorBoardCallback
except ModuleNotFoundError:
    from binancebot.aiml.tensorboard.base_tensorboard import (
        BaseTensorBoardCallback,
        BaseTensorboardLogger,
    )

    TBLogger = BaseTensorboardLogger  # type: ignore
    TBCallback = BaseTensorBoardCallback  # type: ignore

__all__ = ("TBLogger", "TBCallback")
