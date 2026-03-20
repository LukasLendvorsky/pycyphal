from __future__ import annotations

import logging
import typing

ErrorHandler = typing.Callable[[Exception], None]

_error_handler: ErrorHandler | None = None

def set_internal_error_handler(handler: ErrorHandler | None) -> None:
    """
    Register a callback that will be invoked whenever an internal pycyphal component encounters
    an exception somewhere in background asyncio tasks.

    This is useful to be notified when something goes wrong while receiving messages in the background etc.
    
    """
    global _error_handler  # noqa: PLW0603
    _error_handler = handler

def handle_internal_error(logger: logging.Logger, e: Exception, msg: str = "") -> None:
    """
    Report an internal error: log it via the provided *logger* and invoke the registered error handler.

    :param logger: The logger to use for ``logger.exception``.
    :param e: The exception to report.
    :param msg: Optional context message describing where/why the error occurred.

    The handler receives a wrapper :class:`Exception` whose message is *msg* (if provided)
    and whose ``__cause__`` is the original exception *e*.
    """
    logger.exception(msg if msg else e)
    if _error_handler is not None:
        if msg:
            e.add_note(msg)
        _error_handler(e)
        