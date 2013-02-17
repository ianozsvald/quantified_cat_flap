"""Configuration provided by 'import config' and PYTHON_TEMPLATE_CONFIG env var"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import datetime

# Read PYTHON_TEMPLATE_CONFIG environment variable (raise error if missing or badly
# configured), use this to decide on our config and import the relevant python
# file

# This assumes that locally we have suitable python files e.g. production.py,
# testing.py

LOG_FILE = "./catflap.log"

# this error is raised by Twitter if we send a duplicate message
DUPLICATE_MESSAGE_TWITTER_ERROR = u'Status is a duplicate.'

# setup some logging
logger = logging.getLogger('catflap')
log_hdlr = logging.FileHandler(LOG_FILE)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_hdlr.setFormatter(log_formatter)
logger.addHandler(log_hdlr)
logger.setLevel(logging.INFO)

TIME_BETWEEN_EVENTS = datetime.timedelta(seconds=10)


CONFIG_ENV_VAR = "PYTHON_TEMPLATE_CONFIG"
CONFIG_ENV_VAR_PRODUCTION = "production"
CONFIG_ENV_VAR_TESTING = "testing"
config_set = False  # only set to True if we have find a valid ENV VAR
config_choice = os.getenv(CONFIG_ENV_VAR)
if config_choice == CONFIG_ENV_VAR_PRODUCTION or config_choice is None:
    from production import *
    config_set = True
if config_choice == CONFIG_ENV_VAR_TESTING:
    from testing import *
    config_set = True
if not config_set:
    raise ValueError("ALERT! ENV VAR \"{}\" must be set e.g. \"export {}={}\"".format(CONFIG_ENV_VAR, CONFIG_ENV_VAR, CONFIG_ENV_VAR_TESTING))
