#
# by Taka Wang
#

# require by Scanner class
import blescan
import bluetooth._bluetooth as bluez
import time


class Scanner():
    def __init__(self, deviceId = 0, loops = 1):
        self.deviceId = deviceId
        self.loops = loops
        try:
            self.sock = bluez.hci_open_dev(self.deviceId)
            blescan.hci_le_set_scan_parameters(self.sock)
            blescan.hci_enable_le_scan(self.sock)
        except Exception, e:
            print e

    def scan(self):
        return blescan.parse_events(self.sock, self.loops)

    def run(self):
        from cibo.eval_beacon import add_passengers, remove_passengers, \
            Passenger
        while True:
            # Remove duplicate passengers here
            found = set()
            for data in self.scan():
                try:
                    found.add(Passenger(data))
                except:
                    continue
            remove_passengers(found)
            for passenger in found:
                add_passengers(passenger)
            time.sleep(3)

if __name__ == '__main__':
    s = Scanner(loops=10)
    s.run()
