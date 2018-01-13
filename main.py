import pygame, time
from lib import graphiclib, hardwarelib, controllib

configuration = {
    'GAS':5,
    'STOP':2,
    'MUSIC':1,
    'LIGHT':0,
    'VOLIN':5,
    'VOLDE':4,
    'REC':3
}

def main():
    navigator = hardwarelib.Navigator(16)
    print('navigator created')
    light = hardwarelib.Light(15)
    print('light created')
    ultrasonic = hardwarelib.Ultrasonic(11,7)
    print('ultrasonic created')
    temperature = hardwarelib.Temperature()
    print('temperature created')
    camera = graphiclib.PiCamera((500, 0), (500, 1000))
    print('camera created')
    jstick = controllib.Joystick(navigator, light, configuration, camera)
    print('joystic created')

    #pygame stuff
    screen = graphiclib.Screen(size=(1000,1000))
    print('created screen')
    all_sprites = pygame.sprite.RenderUpdates()
    list = graphiclib.List((0,0),(500,1000))
    all_sprites.add(list)
    all_sprites.add(camera)
    clock = pygame.time.Clock()
    running = True
    print('in running loop')

    while running:
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dict = jstick.handle()
        list.set_dict(dict)
        all_sprites.update()
        update_rects = all_sprites.draw(screen.screen)
        screen.refresh(rectangles= update_rects)
    pygame.quit()


if __name__ == '__main__':
    main()