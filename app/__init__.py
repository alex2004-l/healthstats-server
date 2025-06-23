import os
import time
import logging
from logging.handlers import RotatingFileHandler
from threading import Lock
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()
webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

logger = logging.getLogger("webserver_logger")
logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler("webserver.log", maxBytes=1024 * 1024, backupCount=10)
formatter = logging.Formatter('[%(asctime)s] : %(levelname)s - Function : %(funcName)s - %(message)s')
formatter.converter = time.gmtime

handler.setFormatter(formatter)
logger.addHandler(handler)

webserver.logger = logger

webserver.job_counter = 1
webserver.job_lock = Lock()

from app import routes
