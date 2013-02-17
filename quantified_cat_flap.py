"""1 liner to explain this project"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://www.python.org/dev/peps/pep-0263/
import argparse
import logging
import time
import config  # assumes env var PYTHON_TEMPLATE_CONFIG is configured
import RPi.GPIO as GPIO

# Usage:
# $ PYTHON_TEMPLATE_CONFIG=production python start_here.py --help
# $ PYTHON_TEMPLATE_CONFIG=production python start_here.py hello -o bob


logger = logging.getLogger('catflap')
log_hdlr = logging.FileHandler(config.LOG_FILE)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_hdlr.setFormatter(log_formatter)
logger.addHandler(log_hdlr)
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    #parser.add_argument('positional_arg', help='required positional argument')
    #parser.add_argument('--optional_arg', '-o', help='optional argument', default="Ian")

    args = parser.parse_args()
    #print "These are our args:"
    print args
    #print "{} {}".format(args.positional_arg, args.optional_arg)

    logger.info("Starting up")

    PIN_INPUT_1 = 3  # GPIO 0 (SDA), bottom row, second pin after P1 notch
    PIN_GROUND = 6  # GROUND, top row, third pin after P1 notch

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_INPUT_1, GPIO.IN, GPIO.PUD_UP)
    input_1 = GPIO.input(PIN_INPUT_1)
    while True:
        input_1_new = GPIO.input(PIN_INPUT_1)
        if input_1_new != input_1:
            logger.info("Pin changed from %s to %s" % (str(input_1), str(input_1_new)))
        input_1 = input_1_new
        time.sleep(0.05)
