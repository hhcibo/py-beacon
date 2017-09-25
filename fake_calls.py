import datetime
import requests
import time

BACKEND = "http://207.154.234.13:80/"
message_one = {
    "uuid": "8ec1f7b1-28ce-4bee-8acc-20d77f38e5b1",
    "startTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
res = requests.post(BACKEND, data=message_one)
print res.status_code
time.sleep(5)
message_two = {
    "uuid": "8ec1f7b1-28ce-4bee-8acc-20d77f38e5b1",
    "endTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
res = requests.post(BACKEND, data=message_two)
print res.status_code
