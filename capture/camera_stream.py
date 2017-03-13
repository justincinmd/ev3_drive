import io
import socket
import struct
import time
import picamera


image_size = (160, 120)

# See https://picamera.readthedocs.io/en/release-1.13/recipes2.html#rapid-capture-and-streaming
class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)


while True:
    try:
        client_socket = socket.socket()
        client_socket.connect(('jcnnghm-linux.local', 5000))
        connection = client_socket.makefile('wb')
        try:
            output = SplitFrames(connection)
            with picamera.PiCamera(resolution=(160,120), framerate=30) as camera:
                time.sleep(2)
                start = time.time()
                try:
                    camera.start_recording(output, format='mjpeg')
                    while True:
                        camera.wait_recording(30)
                finally:
                    camera.stop_recording()
        finally:
            # Write the terminating 0-length to the connection to let the
            # server know we're done
            try:
                connection.write(struct.pack('<L', 0))
                connection.close()
                client_socket.close()
            finally:
                finish = time.time()
                print('Sent %d images in %d seconds at %.2ffps' % (
                    output.count, finish-start, output.count / (finish-start)))
    except KeyboardInterrupt:
        break
    except socket.error:
        print "No Connection, sleeping"
        time.sleep(0.1)
