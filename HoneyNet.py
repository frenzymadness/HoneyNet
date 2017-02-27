#!/usr/bin/env python3
from configparser import ConfigParser
import importlib
import logging

# Read configuration for all modules
config = ConfigParser()
config.read('config.cfg')

# Logging set up
logging.basicConfig(level=getattr(logging, config['main']['loglevel']))
logger = logging.getLogger(__name__)

workers = []

# For every plugin in config file
for plugin in config:
    if plugin in ('main', 'DEFAULT'):
        continue
    # Import module
    module = importlib.import_module('plugins.' + plugin)
    logging.debug('Imported module {}'.format(plugin))
    # Get main class
    worker_class = module.__dict__[plugin]
    # How many workers we need from this plugin?
    num = int(config[plugin].get('workers', 1))
    # Create as many intances as defined in config file
    for x in range(num):
        logging.debug('{} - creating worker {}'.format(plugin, x))
        # Initialize class (create worker object)
        worker = worker_class(config[plugin])
        # Add worker to the pool of workers
        workers.append(worker)

# Start all workers
logging.info('Starting workers')
for worker in workers:
    worker.start()

logging.info('Joining workers')
# Wait for the end of all workers
for worker in workers:
    worker.join()
