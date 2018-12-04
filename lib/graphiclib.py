import picamera
import picamera.array
import pygame
import pygame.camera
from pygame import *


def render_text_line(rimage, rcolor, rfont, text, pos=(0, 0)):
    render_text = rfont.render(text, 1, rcolor)
    rimage.blit(render_text, pos)


class Screen:
    """The Screen for the Terminal"""

    def __init__(self, size=(100, 100), title="Screen"):
        self.fullscreen = True
        pygame.display.init()
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(title)

    @staticmethod
    def refresh(rectangles=None):
        pygame.display.update(rectangles)

    def toggle_fullscreen(self):
        if self.fullscreen:
            pygame.display.set_mode(self.size)
            self.fullscreen = False
        else:
            displayinfo = pygame.display.Info()
            fullsize = (displayinfo.current_w, displayinfo.current_h)
            pygame.display.set_mode(fullsize, FULLSCREEN | DOUBLEBUF)


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
        self.display_dict = {}
        self.updated = True
        self.txtsize = self.font.size('__||__')

    def set_dict(self, dispdict):
        self.display_dict = dispdict
        self.updated = True

    def update(self):
        if self.updated:
            height = 0
            self.image.fill((0, 0, 0))

            for dictkey in self.display_dict.keys():
                line = '{}: {}'.format(dictkey, self.display_dict[dictkey])
                render_text_line(self.image, (255, 255, 255), self.font, line, (0, height))
                height += self.txtsize[1]

            self.updated = False


class PiCamera(pygame.sprite.Sprite):
    """The Picamera as pygame cam"""

    def __init__(self, position, size):
        pygame.sprite.Sprite.__init__(self)
        pygame.camera.init()
        camera = picamera.PiCamera()
        self.camsize = (size[0], int(size[0]/2))
        camera.resolution = self.camsize
        self.camera = camera
        self.output = picamera.array.PiRGBArray(camera, size=self.camsize)
        self.size = size
        self.image = pygame.Surface(self.size)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self, *args):
        pass

    def new_frame(self):
        self.output.truncate(0)
        self.camera.capture(self.output, 'rgb', resize=self.camsize)
        s = pygame.transform.rotate(pygame.surfarray.make_surface(self.output.array), 270)
        self.image.blit(s, (0, 0))
