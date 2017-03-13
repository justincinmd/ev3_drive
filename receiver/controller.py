import pygame
import sys

if sys.platform != 'darwin':
    # Linux
    L_TRIGGER = 2
    R_TRIGGER = 5
    A_BUTTON = 0
else:
    # OSX
    L_TRIGGER = 4
    R_TRIGGER = 5
    A_BUTTON = 11


class ManualControl(object):
    """Helper class that makes it easy to collect input from an xbox controller
    """
    def __init__(self):
        """Intializes an xbox 360 joystick, as the first connected joystick."""
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_events(self):
        """Yields all incoming control events.  Processing events is
        neccessary to so the get_* joystick calls return correct values.  One
        of process_events or get_events must be called in each control loop.
        """
        for event in pygame.event.get():
            yield event

    def process_events(self):
        """Ignores all incoming control events.  Getting events is
        neccessary to so the get_* joystick calls return correct values.  One
        of process_events or get_events must be called in each control loop.
        """
        for event in self.get_events():
            pass

    def get_throttle(self):
        """Returns throttle from -1.0 to 1.0 using the left and right trigger on
        the xbox controller.
        """
        print self.joystick.get_axis(R_TRIGGER)
        print self.joystick.get_axis(L_TRIGGER)
        return ((self.joystick.get_axis(R_TRIGGER) + 1.0) / 2.0) - ((self.joystick.get_axis(L_TRIGGER) + 1.0) / 2.0)

    def get_angle(self):
        """Steering angle is from the horizontal movement of the left
        joystick of the xbox controller.  This returns values from -0.5 to
        0.5 instead of -1 to 1 to prevent excessive oversteering.
        """
        return self.joystick.get_axis(0)

    def is_manual_control(self):
        """Detects holding the A button on the xbox controller."""
        return self.joystick.get_button(A_BUTTON)

    def __str__(self):
        return "Throttle: {}\nAngle: {}\nManual Control: {}\n".format(
            self.get_throttle(),
            self.get_angle(),
            self.is_manual_control()
        )
