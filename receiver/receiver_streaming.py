import json
import time
from cStringIO import StringIO
import pygame.display
import pygame.image
from PIL import Image
from controller import ManualControl
import socket
import struct
import io
import Queue
import threading

image_size = (160, 120)
pygame.display.init()
screen = pygame.display.set_mode(image_size)
# pygame.display.set_caption('EV3')
pygame.display.flip()
control = ManualControl()
running = True


queue = Queue.Queue()


def process_image(data):
    img = Image.open(StringIO(data))
    surface = pygame.image.fromstring(img.tobytes('raw', 'RGB'), image_size, 'RGB')
    screen.fill((0, 0, 0))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    control.process_events()
    print control.get_throttle(), control.get_angle()


def run_server():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(0)

    try:
        while running:
            # Accept a single connection and make a file-like object out of it
            connection = server_socket.accept()[0].makefile('rb')
            try:
                while running:
                    # Read the length of the image as a 32-bit unsigned int. If the
                    # length is zero, quit the loop
                    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                    if not image_len:
                        break
                    queue.put(connection.read(image_len))
            finally:
                connection.close()
    finally:
        server_socket.close()


t = threading.Thread(target=run_server)
t.start()

try:
    queue.get(block=True)
    start_time = time.time()
    received_frames = 0
    skipped_frames = 0
    while True:
        next_image = queue.get(block=True)
        received_frames += 1
        if not queue.empty():
            skipped_frames += 1
            continue
        process_image(next_image)
finally:
    end_time = time.time()
    running = False
    elapsed = end_time - start_time
    print "Received %d frames in %.2f seconds, skipping %d" % (received_frames, elapsed, skipped_frames)
    print "Received FPS: %.2f, Effective FPS: %.2f" % (received_frames/elapsed, (received_frames-skipped_frames)/elapsed)
    t.join()
