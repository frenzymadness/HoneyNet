#!/usr/bin/env python3
from configparser import ConfigParser
import os
import importlib

# Read configuration for all modules
config = ConfigParser()
config.read('config.cfg')

# Get plugin list from folder 'plugins'
plugins_list = os.listdir('plugins')
plugins_list.remove('__init__.py')
plugins_list.remove('__pycache__')
plugins_list = [plugin.rstrip('.py') for plugin in plugins_list]

workers = []

# For every plugin in folder
for plugin in plugins_list:
    # Import module
    module = importlib.import_module('plugins.' + plugin)
    # Get main class
    worker_class = module.__dict__[plugin]
    # Initialize class (create worker object)
    worker = worker_class(config[plugin])
    # Add worker to the pool of workers
    workers.append(worker)

print(workers)
