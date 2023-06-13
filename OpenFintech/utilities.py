import logging 
# TODO: Implement code within create_logger to clean logs


def create_logger(filename:str=None, format:str='%(asctime)s/%(name)s/%(levelname)s:: %(message)s'):
    if filename==None: raise Exception("Filename required.")
    # Setup logger and level
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create the stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Create the file handler
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.ERROR)

    # Create formatter and add it to the file and stream handler
    formatter = logging.Formatter(format)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
