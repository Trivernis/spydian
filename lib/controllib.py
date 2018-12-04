import os
import pygame


class Joystick:
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

    def _button_check(self, name, i, c, button):
        """ Checks if a button was pressed and wasn't pressed before. """
        if i == c[name]:
            if button == 1 and i not in self.pressed:
                self.pressed.append(i)
                return 1
            elif button == 0 and i in self.pressed:
                self.pressed.remove(i)
                return 2
        return 0

    def _handle_buttons(self, axis_dict, c):
        for i in range(self.joystick.get_numbuttons()):
            button = self.joystick.get_button(i)
            axis_dict['Button {}'.format(i)] = button

            if self._button_check('LIGHT', i, c, button) == 1:
                self.light.switch()

            elif self._button_check('MUSIC', i, c, button) == 1:
                if self.splaying:
                    self.sound.stop()
                    self.splaying = False
                else:
                    self.sound.play()
                    self.splaying = True

            elif self._button_check('VOLIN', i, c, button) == 1:
                self.sound.set_volume(self.sound.get_volume() + 0.1)
            elif self._button_check('VOLIN', i, c, button) == 2:
                self.sound.set_volume(self.sound.get_volume() - 0.1)

            elif self._button_check('VOLDE', i, c, button):
                pass

            elif self._button_check('REC', i, c, button) == 1:
                self._save_camimg()
        return axis_dict

    def handle(self):
        c = self.configuration
        nav = self.navigator
        axis_dict = {}
        # axes
        for i in range(self.joystick.get_numaxes()):
            axis = self.joystick.get_axis(i)
            axis_dict['Axis {}'.format(i)] = axis

            if i == c['GAS'] and axis > 0.1:
                nav.forward()
            elif i == c['GAS'] and axis < 0.1:
                nav.stop()
        axis_dict = self._handle_buttons(axis_dict, c)
        # hats
        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            axis_dict['Hat {}'.format(i)] = hat

            if hat == (-1, 0):
                nav.left()
            elif hat == (1, 0):
                nav.right()
            else:
                nav.straight()

        axis_dict['Volume'] = self.sound.get_volume()
        return axis_dict

    def _save_camimg(self):
        self.camera.new_frame()
        img = self.camera.image
        if os.path.isfile('image.jpg'):
            count = 0
            while os.path.isfile('./images/img{}.jpg'.format(count)):
                count += 1
            os.rename('image.jpg', 'images/img{}.jpg'.format(count))
        pygame.image.save(img, 'image.jpg')
