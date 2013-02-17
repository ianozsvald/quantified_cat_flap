"""1 liner to explain this project"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://www.python.org/dev/peps/pep-0263/
import argparse
import datetime
import logging
import time
import random
import config  # assumes env var PYTHON_TEMPLATE_CONFIG is configured
import RPi.GPIO as GPIO
import twitter
from twitter_tokens import *  # not git controlled

# Usage:
# $ PYTHON_TEMPLATE_CONFIG=production python start_here.py --help
# $ PYTHON_TEMPLATE_CONFIG=production python start_here.py hello -o bob

# PROBLEMS:
# entirely untested at present!
# make the gpio read a generator, yield status, if_status_changed,
# time_delta_for_change
# use a list of events for testing
# post an event to an internal Queue for 'use', the only current use will be
# to post to twitter (but we can get Queue item and test it)


twitter_api = twitter.Api(consumer_key=CONSUMER_KEY,
                          consumer_secret=CONSUMER_SECRET,
                          access_token_key=ACCESS_TOKEN,
                          access_token_secret=ACCESS_TOKEN_SECRET)


logger = logging.getLogger('catflap')
log_hdlr = logging.FileHandler(config.LOG_FILE)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_hdlr.setFormatter(log_formatter)
logger.addHandler(log_hdlr)
logger.setLevel(logging.INFO)


def post_update():
    hash_tag = "#catflatreport"
    msgs = ["%s: kitty stretching legs" % (hash_tag),
            "%s: is that ANOTHER worm?!" % (hash_tag),
            "%s: kitty sees something moving out there" % (hash_tag),
            "%s: chase Polly chase!" % (hash_tag),
            "%s: up the tree up the tree!" % (hash_tag),
            "%s: maybe time to curl up and rest now" % (hash_tag)]
    msg = random.choice(msgs)
    twitter_api.PostUpdate(msg)


if __name__ == "__main__X":
    post_update()


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

    time_of_last_event = datetime.datetime.utcnow()
    TIME_BETWEEN_EVENTS = datetime.timedelta(seconds=5)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_INPUT_1, GPIO.IN, GPIO.PUD_UP)
    input_1 = GPIO.input(PIN_INPUT_1)
    while True:
        input_1_new = GPIO.input(PIN_INPUT_1)
        if input_1_new != input_1:
            logger.info("Pin changed from %s to %s" % (str(input_1), str(input_1_new)))
            time_of_new_event = datetime.datetime.utcnow()
            time_delta = time_of_new_event - time_of_last_event
            if time_delta > TIME_BETWEEN_EVENTS:
                time_of_last_event = time_of_new_event
                post_update()
        input_1 = input_1_new
        time.sleep(0.05)
