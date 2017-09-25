#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import requests.exceptions
import time
import logging
import datetime

log = logging.getLogger(__name__)

IN_VEHICLE = {}
THRESHOLD = 15

BACKEND = "http://207.154.234.13:80/"
json_time_key_mapping = {"start": "startTime", "end": "endTime"}


class Passenger(object):

    def __init__(self, ble_data):
        self.uuid = ble_data
        # We need to set a timezone, or at least now the default we use here
        # if we send it to the backend
        self.time = time.time()
        self.expire_time = int(time.time()) + THRESHOLD

    def reset_expire_time(self):
        self.expire_time = int(time.time()) + THRESHOLD


def send_to_backend(passenger, type):
    # For Demo Reasons only use our Testbeacon
    if "8ec1f7b1-28ce-4bee-8acc" in passenger.uuid:
        try:
            key = json_time_key_mapping.get(type)
            message = {
                "uuid": passenger.uuid,
                key: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            requests.post(BACKEND, data=message)
        except requests.exceptions.ConnectionError, e:
            print "Could not post to endpoint %s" % BACKEND
            print e


def remove_passengers(found):
    """Remove expire beacons"""
    now = int(time.time())
    for id in IN_VEHICLE.keys():
        if IN_VEHICLE[id].expire_time < now:
            passenger = IN_VEHICLE[id]
            del IN_VEHICLE[id]
            send_to_backend(passenger, 'end')


def add_passengers(passenger):
    if passenger.uuid not in IN_VEHICLE:
        IN_VEHICLE[passenger.uuid] = passenger
        send_to_backend(passenger, 'start')
    passenger.reset_expire_time()
