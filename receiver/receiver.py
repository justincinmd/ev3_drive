import json
from cStringIO import StringIO
from flask import Flask
from flask import request
import pygame.display
import pygame.image
from PIL import Image
from controller import ManualControl

pygame.display.init()
screen = pygame.display.set_mode((160, 120))
# pygame.display.set_caption('EV3')
pygame.display.flip()
app = Flask(__name__)
image_size = (160, 120)
control = ManualControl()


@app.route('/', methods=('POST',))
def process_image():
    data = request.data
    print "Received Image: ", len(data), " bytes"
    img = Image.open(StringIO(data))
    surface = pygame.image.fromstring(img.tobytes('raw', 'RGB'), image_size, 'RGB')
    screen.fill((0, 0, 0))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    control.process_events()
    return json.dumps({'throttle': control.get_throttle(), 'angle': control.get_angle()})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
