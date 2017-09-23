#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
log = logging.getLogger(__name__)

IN_VEHICLE = {}
THRESHOLD = 5


class BLEMessage(object):

    def __init__(self, unformatted_string):
        splitted = unformatted_string.split(",")
        self.address = splitted[1]
        # We need to set a timezone, or at least now the default we use here
        self.time = time.time()
        self.dezibel = splitted[-1]


class Passenger(object):

    def __init__(self, uuid):
        self.uuid = uuid
        self.expire_time = int(time.time()) + THRESHOLD


def send_to_backend(message, type):
    # Post request to backend
    print message
    print type


def remove_passengers(found):
    """Remove expire beacons"""
    now = int(time.time())
    for id in IN_VEHICLE.keys():
        if IN_VEHICLE[id].expire_time < now:
            del IN_VEHICLE[id]
            print("Passenger left ", str(id))
            send_to_backend(id, 'remove')


def add_passengers(beacon):
    try:
        message = BLEMessage(beacon)
    except Exception, e:
        log.error(e)
        return
    if message.address not in IN_VEHICLE:
        passenger = Passenger(message.address)
        IN_VEHICLE[message.address] = passenger
        send_to_backend(message, 'start')
        #reset_expire_time_of Passenger
