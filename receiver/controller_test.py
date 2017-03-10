from controller import ManualControl
import time

control = ManualControl()

while True:
    control.process_events()
    print control
    time.sleep(0.1)
