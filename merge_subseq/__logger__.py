import logging
from .__common__ import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)
