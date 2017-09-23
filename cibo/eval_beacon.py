#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pendulum
from mock import patch
import beacon_empfang
import logging
log = logging.getLogger(__name__)

IN_VEHICLE = {}

data = """ed:60:ae:91:2a:7f,6492828243f84ba5b3ef794f77040af5,20000,44689,-60,-69
        ed:9a:e4:ed:ee:b6,6492828243f84ba5b3ef794f77040af5,2,4,-60,-57
        e7:2d:34:ad:2b:cd,b9407f30f5f8466eaff925556b57fe6d,10000,13485,-60,-76
        5a:a2:3a:f3:57:e8,0613ff4c000c0e00c1edbef54fd23a45,47095,32107,83,-65
        5a:a2:3a:f3:57:e8,0613ff4c000c0e00c1edbef54fd23a45,47095,32107,83,-65
        ed:9a:e4:ed:ee:b6,6492828243f84ba5b3ef794f77040af5,2,4,-60,-58
        ed:9a:e4:ed:ee:b6,6492828243f84ba5b3ef794f77040af5,2,4,-60,-58
        5a:a2:3a:f3:57:e8,0613ff4c000c0e00c1edbef54fd23a45,47095,32107,83,-65
        62:b3:d2:1f:28:eb,010001eb281fd2b3620b02010607ff4c,16,523,0,-74
        5a:a2:3a:f3:57:e8,0613ff4c000c0e00c1edbef54fd23a45,47095,32107,83,-65
        5a:a2:3a:f3:57:e8,0613ff4c000c0e00c1edbef54fd23a45,47095,32107,83,-64
        ed:9a:e4:ed:ee:b6,6492828243f84ba5b3ef794f77040af5,2,4,-60,-57
        5a:a2:3a:f3:57:e8,0613ff4c000c0e00c1edbef54fd23a45,47095,32107,83,-65
        e7:2d:34:ad:2b:cd,b9407f30f5f8466eaff925556b57fe6d,10000,13485,-60,-74
        5a:a2:3a:f3:57:e8,0613ff4c000c0e00c1edbef54fd23a45,47095,32107,83,-65"""
splitted = [x.strip() for x in data.split("\n")]


def test_data():
    mess = BLEMessage(splitted[0])
    print mess.address, mess.dezibel


class BLEMessage(object):

    def __init__(self, unformatted_string):
        splitted = unformatted_string.split(",")
        self.address = splitted[1]
        # We need to set a timezone, or at least now the default we use here
        self.time = pendulum.now()
        self.dezibel = splitted[-1]


class Passenger(object):

    def __init__(self, uuid):
        self.uuid = uuid
        self.counter = 0

    def reset_counter(self):
        self.counter = 0


def send_to_backend(message, type):
    # Post request to backend
    print message.address


def remove_passengers(found):
    print found


def add_passengers(beacon):
    try:
        message = BLEMessage(beacon)
    except Exception, e:
        log.error(e)
        return
    if message.address not in IN_VEHICLE:
        passenger = Passenger(message.address)
        passenger.counter += 1
        IN_VEHICLE[message.address] = passenger
        print passenger.counter
        send_to_backend(message, 'start')
    # reset_expire_time_of Passenger
