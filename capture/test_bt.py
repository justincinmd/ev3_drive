import time

# command to start motor on port A at speed 20
start_motor = '\x0C\x00\x00\x00\x80\x00\x00\xA4\x00\x01\x14\xA6\x00\x01'

# command to stop motor on port A
stop_motor = '\x09\x00\x01\x00\x80\x00\x00\xA3\x00\x01\x00'

# send commands to EV3 via bluetooth
with open('/dev/rfcomm0', 'w', 0) as bt:
    bt.write(start_motor)
    time.sleep(5)
    bt.write(stop_motor)
