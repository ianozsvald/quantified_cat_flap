"""1 liner to explain this project"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://www.python.org/dev/peps/pep-0263/
import argparse
import datetime
import time
import random
import config  # assumes env var PYTHON_TEMPLATE_CONFIG is configured
try:
    import RPi.GPIO as GPIO
except:
    print "Problem on import of RPi.GPIO - are we not on a RaspberryPi?"

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

logger = config.logger
PIN_INPUT_1 = 3  # GPIO 0 (SDA), bottom row, second pin after P1 notch
PIN_GROUND = 6  # GROUND, top row, third pin after P1 notch


def post_update(last_message_posted):
    """Send a message to Twitter"""
    hash_tag = "#catflapbot"
    MAX_LOOP = 5
    nbr_looped = 0
    while True:
        nbr_looped += 1
        #msgs = ["%s: Polly stretches legs" % (hash_tag)]  # for debug
        msgs = ["%s: Polly stretches legs" % (hash_tag)]
                "%s: Polly! Is that ANOTHER worm?!" % (hash_tag),
                "%s: do you see something moving out there?" % (hash_tag),
                "%s: chase Polly chase!" % (hash_tag),
                "%s: up the tree up the tree!" % (hash_tag),
                "%s: Polly decides it is time to curl up and rest now" % (hash_tag)]
        msg = random.choice(msgs)
        sent_ok = False
        try:
            config.twitter_api.PostUpdate(msg)
            logger.info("Msg '%s' sent to Twitter" % (str(msg)))
            sent_ok = True
        except config.twitter.TwitterError as err:
            if err.message == config.DUPLICATE_MESSAGE_TWITTER_ERROR:
                # we've posted a duplicate message - try again
                logger.info("We have sent a duplicate to Twitter: %s" % (str(err)))
            else:
                logger.info("Twitter error: %s" % (str(err)))
        if sent_ok:
            break
        if nbr_looped > MAX_LOOP:
            logger.error("We looped too many times for post_update, bailing (is something wrong with Twitter?)")
            break
    return msg


def loop():
    time_of_last_event = datetime.datetime.utcnow()
    last_message_posted = None
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_INPUT_1, GPIO.IN, GPIO.PUD_UP)
    input_1 = GPIO.input(PIN_INPUT_1)
    while True:
        input_1_new = GPIO.input(PIN_INPUT_1)
        if input_1_new != input_1:
            logger.info("Pin changed from %s to %s" % (str(input_1), str(input_1_new)))
            time_of_new_event = datetime.datetime.utcnow()
            time_delta = time_of_new_event - time_of_last_event
            if time_delta > config.TIME_BETWEEN_EVENTS:
                time_of_last_event = time_of_new_event
                last_message_posted = post_update(last_message_posted)
        input_1 = input_1_new
        time.sleep(0.05)


if __name__ == "__main__X":
    last_message_posted = None
    last_message_posted = post_update(last_message_posted)
    print last_message_posted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    #parser.add_argument('--optional_arg', '-o', help='optional argument', default="Ian")
    args = parser.parse_args()
    print args

    logger.info("Starting up")
    try:
        loop()
    except Exception as err:
        logger.exception("Caught at the end of the program: %s" % (str(err)))
        raise
