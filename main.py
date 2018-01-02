import pygame, picamera  #,gyro
from lib import ultrasonic
from datetime import datetime
from subprocess import call
import RPi.GPIO as GPIO



# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
# --ultrasonic--
sensor= ultrasonic.Sensor()
sensor.init(11,7)
# -- Nightmode
# WHITE, BLACK=BLACK,WHITE
# Pins BCM
motor = 16
lightpin=15
#
# --config--
use_camera=False
use_gyro_preview=False
#--
forpress = False
light = False
lpress = False
play = False
ppress = False
voluppress = False
voldopress = False
recpress=False
recording=False
left=False
right=False
lastContact=datetime.now()
if use_camera:
    cam = picamera.PiCamera()

top_view = pygame.image.load('top_view.png')
top_view= pygame.transform.scale(top_view, (192, 108))

# Axis
GAS = 5
STOP = 2

# Buttons
MUSIC = 1
LIGHT = 0
VOLUP = 5
VOLDO = 4
RECSTART = 3

# setup the relais
GPIO.setup(motor,GPIO.OUT)
GPIO.setup(lightpin,GPIO.OUT)
GPIO.output(motor,True)
GPIO.output(lightpin, True)
# ____________________________
# -- driving functions
def drive_forw():
    GPIO.output(motor,False)
    return

def drive_backw():
    print(drive_backw)
    return

def reset_dire():
    GPIO.output(motor,True)
    return

def drive_left():
    if not left:
        call(['python', './lib/servolib.py','left'])
    return

def drive_right():
    if not right:
        call(['python', './lib/servolib.py','right'])
    return

def reset_turn():
    if left or right:
        call(['python','./lib/servolib.py'])
    return
# ____________________________
# -- special functions
def turn_light(shine):
    if shine:
        GPIO.output(lightpin, False)
    else:
        GPIO.output(lightpin, True)
    return

def turn_rec(*record):
    #if record:
        #cam.start_recording('record.h264')
        #return
    #else:
        #cam.stop_recording()
        #return
    if use_camera:
        try:
            cam.capture('image.jpg', resize=(192 * 2, 108 * 2))
            cam.capture("./Images/image{}.jpg".format(str(datetime.now()).replace(':','_')))
        except Exception as error:
            print(error)

def imgRefresh():
    #turn_rec(True)
    image = None
    try:
        image = pygame.image.load('image.jpg')
        image = pygame.transform.scale(image, (192*2, 108*2))
    except:
        pass
    screen.blit(image, (500, 10))
    #gyro_output = gyro.getAllOut()
    #rotation = gyro_output['rot']
    if use_gyro_preview:
        top_view = pygame.image.load('top_view.png')
        # The scaling of the top_view Spider
        scal_x = abs(int(192 * ((abs(rotation[0]) / 90) - 1)))
        scal_y = abs(int(108 * ((abs(rotation[1]) / 90) - 1)) - 1)
        top_view = pygame.transform.scale(top_view, (scal_x, scal_y))
        screen.blit(top_view, (550 - (scal_x / 2), 300 - (scal_y / 2)))

def printDriveData():
    textPrint.print(screen,"")
    textPrint.print(screen,"Sound Information")
    textPrint.print(screen, "   Sound: {}".format(play))
    textPrint.print(screen, "   Volume: {}".format(sound.get_volume()))
    textPrint.print(screen, "Light: {}".format(light))
    textPrint.print(screen, "Last Controller Input: {}".format((datetime.now()-lastContact).seconds))
    #gyro_output=gyro.getAllOut()
    #rotation=gyro_output['rot']
    #textPrint.print(screen, "Rotation: X:{}; Y:{}".format(rotation[0],rotation[1]))
    #acceleration = gyro_output['acc_sca']
    #textPrint.print(screen, "Acceleration: X:{}; Y:{}; Z:{}".format(acceleration[0], acceleration[1],acceleration[2]))
    distance=sensor.echo()
    textPrint.print(screen, "Distance: {} cm".format(distance))
    #if distance<40:
    #    turn_rec()

def doSubroutine():
    if abs((datetime.now()-lastContact).seconds)==30:
        print('Contact Lost')
    imgRefresh()

# ____________________________
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    
pygame.init()

# ________________________
# -- music playback
pygame.mixer.init()
sound=pygame.mixer.Sound('./gasgasgas.wav')
sound.set_volume(0.3)
# ________________________
 
# Set the width and height of the screen [width,height]
size = [1000, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("SPYDER STEUERZENTRALE")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()
turn_rec(True)
image=pygame.image.load('image.jpg')
image=pygame.transform.scale(image,(192*2,108*2))
count=0

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTIO
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        #name = joystick.get_name()
        #textPrint.print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
            if i==STOP and axis>0.1:
                print('STOP')
                drive_backw()
                lastContact=datetime.now()
            elif i==GAS and axis>0.1:
                print('GAS')
                if not forpress:
                    drive_forw()
                    forpress=True
                lastContact=datetime.now()
            elif i==GAS and axis<0.1:
                if forpress:
                    reset_dire()
                    print('RESETDRIVE')
                    forpress=False

        textPrint.unindent()
            
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
            if button==1:
                lastContact=datetime.now()
            #if i==7 and button==1:
            #    print('GAS')
            #    drive_forw()
            #elif i==6 and button==1:
            #    print('STOP')
            #    drive_backw()
            if i==LIGHT and button==1 and not lpress:
                light=not light
                lpress=True
                turn_light(light)
                print('Light: {}'.format(light))
            elif i==LIGHT and button==0:
                lpress=False
            elif i==MUSIC and button==1 and not play and not ppress:
                ppress=True
                sound.play()
                play=True
                print('Sound: {}'.format(play))
            elif i==MUSIC and button==1 and play and not ppress:
                ppress=True
                sound.stop()
                play=False
                print('Sound: {}'.format(play))
            elif i==MUSIC and button==0 and ppress:
                ppress=False
            elif i==VOLUP and button==1 and not voluppress:
                sound.set_volume(sound.get_volume()+0.1)
                print('Volume: {}'.format(sound.get_volume()))
                voluppress=True
            elif i==VOLUP and button==0:
                voluppress=False
            elif i== VOLDO and button==0:
                voldopress=False
            elif i==VOLDO and button==1 and not voldopress:
                sound.set_volume(sound.get_volume()-0.1)
                print('Volume: {}'.format(sound.get_volume()))
                voldopress=True
            elif i==RECSTART and button==1 and not recpress:
                recording=not recording
                turn_rec(recording)
                print('Recording: {}'.format(recording))
                recpress=True
            elif i==RECSTART and button==0:
                recpress=False
                
        textPrint.unindent()
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
            if hat==(-1,0):
                print('LEFT')
                drive_left()
                left=True
                right=False
                lastContact=datetime.now()
            elif hat==(1,0):
                print('RIGHT')
                drive_right()
                right=True
                left=False
                lastContact=datetime.now()
            else:
                reset_turn()
                left=False
                right=False
        textPrint.unindent()
        
        textPrint.unindent()

        printDriveData()
        doSubroutine()

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
sensor.clean()
pygame.quit ()
