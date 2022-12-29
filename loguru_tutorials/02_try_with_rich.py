from loguru import logger
from rich.logging import RichHandler
import time

logger.configure(handlers=[{"sink": RichHandler(markup=True), "format": "{message}"}])

logger.debug("This is a debug statement")

time.sleep(1)

logger.info("This is an info statement")
logger.error("This is an error statement")
