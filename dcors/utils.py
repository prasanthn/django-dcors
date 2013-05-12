import logging

# A logger.
logger = logging.getLogger('dcors')
logger.setLevel(logging.WARN)
ch = logging.StreamHandler()
ch.setLevel(logging.WARN)
formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
