import logging
import os

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'tool_log.log')

logger = logging.getLogger()
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler(log_file, mode='w')  # Append mode
file_handler.setLevel(logging.INFO)  # You can adjust the logging level (INFO, DEBUG, etc.)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
