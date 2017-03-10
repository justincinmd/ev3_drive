from cStringIO import StringIO
from flask import Flask
from flask import request
import pygame.display
import pygame.image
from PIL import Image

pygame.display.init()
screen = pygame.display.set_mode((160, 120))
pygame.display.set_caption('EV3')
app = Flask(__name__)
image_size = (160,120)

@app.route('/', methods=('POST',))
def process_image():
    data = request.data
    print "Received Image: ", len(data), " bytes"
    img = Image.open(StringIO(data))
    surface = pygame.image.fromstring(img.tobytes('raw', 'RGB'), image_size, 'RGB')
    screen.blit(surface, (0,0))
    pygame.display.flip()
    return "DONE"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
