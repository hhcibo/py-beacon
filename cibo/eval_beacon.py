#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
log = logging.getLogger(__name__)

IN_VEHICLE = {}
THRESHOLD = 15


class Passenger(object):

    def __init__(self, ble_data):
        self.uuid = ble_data
        # We need to set a timezone, or at least now the default we use here
        # if we send it to the backend
        self.time = time.time()
        self.expire_time = int(time.time()) + THRESHOLD

    def reset_expire_time(self):
        self.expire_time = int(time.time()) + THRESHOLD

    def __hash__(self):
        return hash(self.uuid)


def send_to_backend(uuid, type):
    # Post request to backend
    if "8ec1f" in uuid:
        print type
        print uuid


def remove_passengers(found):
    """Remove expire beacons"""
    now = int(time.time())
    for id in IN_VEHICLE.keys():
        if IN_VEHICLE[id].expire_time < now:
            del IN_VEHICLE[id]
            print("Passenger left ", str(id))
            send_to_backend(id, 'remove')


def add_passengers(passenger):
    if passenger.uuid not in IN_VEHICLE:
        IN_VEHICLE[passenger.uuid] = passenger
        send_to_backend(passenger.uuid, 'start')
        print("Passenger appeared ", str(passenger.uuid))
    passenger.reset_expire_time()
