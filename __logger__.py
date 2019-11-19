import logging
logger = logging.getLogger('merge_sub_sequence')

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)
