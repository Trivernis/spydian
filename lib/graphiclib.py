import pygame, pygame.camera
import picamera
import picamera.array
from pygame import *


def render_text_line(image, color, font, text, pos=(0, 0)):
    render_text = font.render(text, 1, color)
    image.blit(render_text, pos)


class Screen:
    """The Screen for the Terminal"""

    def __init__(self, size=(100, 100), title="Screen"):
        pygame.display.init()
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(title)

    def refresh(self, rectangles=None):
        pygame.display.update(rectangles)

    def toggle_fullscreen(self):
        if self.fullscreen:
            pygame.display.set_mode(self.size)
            self.fullscreen = False
        else:
            displayinfo = pygame.display.Info()
            fullsize = (displayinfo.current_w, displayinfo.current_h)
            pygame.display.set_mode(fullsize, FULLSCREEN | DOUBLEBUF)
            self.fullscreen = True


class List(pygame.sprite.Sprite):
    """A List that shows the values of the terminal"""

    def __init__(self, position, size):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        self.size = size
        self.image = pygame.Surface(self.size)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.font = pygame.font.SysFont('Arial', 25)
        self.dict = {}
        self.updated = True
        self.txtsize = self.font.size('__||__')

    def set_dict(self, dict):
        self.dict = dict
        self.updated = True

    def update(self, *args):
        if self.updated:
            height = 0
            self.image.fill((0, 0, 0))

            for key in self.dict.keys():
                line = '{}: {}'.format(key, self.dict[key])
                render_text_line(self.image, (255, 255, 255), self.font, line, (0, height))
                height += self.txtsize[1]

            self.updated = False
        print('update function called')


class PiCamera(pygame.sprite.Sprite):
    """The Picamera as pygame cam"""

    def __init__(self, position, size):
        pygame.sprite.Sprite.__init__(self)
        pygame.camera.init()
        camera = picamera.PiCamera()
        self.camera = camera
        self.output = picamera.array.PiRGBArray(camera, size=size)
        self.size = size
        self.image = pygame.Surface(self.size)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self, *args):
        print('updating camera')
        self.output.truncate(0)
        self.camera.capture(self.output, 'rgb')
        s = pygame.transform.rotate(pygame.surfarray.make_surface(self.output.array), 90)
        self.image.blit(s, (0, 0))