import pygame
import time
from lib import graphiclib, hardwarelib, controllib

configuration = {
    'GAS': 5,
    'STOP': 2,
    'MUSIC': 1,
    'LIGHT': 0,
    'VOLIN': 5,
    'VOLDE': 4,
    'REC': 3
}


def main():
    navigator = hardwarelib.Navigator(16)
    light = hardwarelib.Light(15)
    ultrasonic = hardwarelib.Ultrasonic(11, 7)
    temperature = hardwarelib.Temperature()
    camera = graphiclib.PiCamera((500, 0), (500, 1000))
    jstick = controllib.Joystick(navigator, light, configuration, camera)

    # pygame stuff
    screen = graphiclib.Screen(size=(1000, 1000))
    all_sprites = pygame.sprite.RenderUpdates()
    glist = graphiclib.List((0, 0), (500, 1000))
    all_sprites.add(glist)
    all_sprites.add(camera)
    clock = pygame.time.Clock()
    running = True

    while running:

        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('quit event')
                running = False

        gdict = jstick.handle()
        gdict['Distance'] = ultrasonic.get_distance()
        glist.set_dict(gdict)
        all_sprites.update()
        update_rects = all_sprites.draw(screen.screen)
        screen.refresh(rectangles=update_rects)
    pygame.quit()


if __name__ == '__main__':
    main()
