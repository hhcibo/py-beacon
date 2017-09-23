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
            found = []
            without_dupes = []
            for data in self.scan():
                try:
                    splitted = data.split(",")
                    if splitted[1] not in found and int(splitted[-1]) >= -50 :
                        found.append(splitted[1])
                        without_dupes.append(Passenger(splitted[1]))
                        print splitted
                except Exception, e:
                    print e
            remove_passengers(found)
            for passenger in without_dupes:
                add_passengers(passenger)
            time.sleep(3)

if __name__ == '__main__':
    s = Scanner(loops=10)
    s.run()
