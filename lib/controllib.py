import os
import pygame


class Joystick():
    def __init__(self, navigator, light, configuration, camera):
        # joystick
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        # sound
        pygame.mixer.init()
        sound = pygame.mixer.Sound('./sounds/gasgasgas.wav')
        sound.set_volume(0.3)
        self.camera = camera
        self.sound = sound
        self.joystick = joystick
        self.navigator = navigator
        self.light = light
        self.configuration = configuration
        self.pressed = []
        self.splaying = False

    def handle(self):
        c = self.configuration
        nav = self.navigator
        dict = {}
        # axes
        for i in range(self.joystick.get_numaxes()):
            axis = self.joystick.get_axis(i)
            dict['Axis {}'.format(i)] = axis

            if i == c['GAS'] and axis > 0.1:
                nav.forward()
            elif i == c['GAS'] and axis < 0.1:
                nav.stop()
        # buttons
        for i in range(self.joystick.get_numbuttons()):
            button = self.joystick.get_button(i)
            dict['Button {}'.format(i)] = button

            if i == c['LIGHT'] and button == 1 and i not in self.pressed:
                self.light.switch()
                self.pressed.append(i)
            elif i == c['LIGHT'] and button == 0 and i in self.pressed:
                self.pressed.remove(i)

            elif i == c['MUSIC'] and button == 1 and i not in self.pressed:
                if self.splaying:
                    self.sound.stop()
                    self.splaying = False
                else:
                    self.sound.play()
                    self.splaying = True
                self.pressed.append(i)
            elif i == c['MUSIC'] and button == 0 and i in self.pressed:
                self.pressed.remove(i)

            elif i == c['VOLIN'] and button == 1 and i not in self.pressed:
                self.sound.set_volume(self.sound.get_volume() + 0.1)
                self.pressed.append(i)
            elif i == c['VOLIN'] and button == 0 and i in self.pressed:
                self.sound.set_volume(self.sound.get_volume() - 0.1)
                self.pressed.remove(i)

            elif i == c['VOLDE'] and button == 1 and i not in self.pressed:
                self.pressed.append(i)
            elif i == c['VOLDE'] and button == 0 and i in self.pressed:
                self.pressed.remove(i)

            elif i == c['REC'] and button == 1 and i not in self.pressed:
                self._save_camimg()
                self.pressed.append(i)
            elif i == c['REC'] and button == 0 and i in self.pressed:
                self.pressed.remove(i)

        # hats
        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            dict['Hat {}'.format(i)] = hat

            if hat == (-1, 0):
                nav.left()
            elif hat == (1, 0):
                nav.right()
            else:
                nav.straight()

        dict['Volume'] = self.sound.get_volume()
        return dict

    def _save_camimg(self):
        self.camera.new_frame()
        img = self.camera.image
        if os.path.isfile('image.jpg'):
            count = 0
            while os.path.isfile('./images/img{}.jpg'.format(count)):
                count += 1
            os.rename('image.jpg', 'images/img{}.jpg'.format(count))
        pygame.image.save(img, 'image.jpg')
