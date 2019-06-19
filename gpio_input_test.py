import RPi.GPIO as GPIO
import time
import os

# Set GPIO pin definition
GPIO.setmode(GPIO.BCM)

hibeam_ch = 2
lturn_ch = 3
rturn_ch = 4
start_thik_ch = 17
reverse_suste_ch = 27
babbal_ch = 22

GPIO.setup(hibeam_ch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lturn_ch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rturn_ch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_thik_ch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reverse_suste_ch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(babbal_ch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

hibeam = 0
lturn = 0
rturn = 0
mode = 'standby'
drive = 0
hold_time = 0
just_switched = 0

def get_gpio(veh_speed):
    global hibeam
    global lturn
    global rturn
    global mode
    global drive
    global start
    global end
    global hold_time
    global just_switched
    
    if GPIO.input(hibeam_ch) == 0:
        hibeam = 1
    else:
        hibeam = 0
    if GPIO.input(lturn_ch) == 0:
        lturn = 1
    else:
        lturn = 0
    if GPIO.input(rturn_ch) == 0:
        rturn = 1
    else:
        rturn = 0
        
    if drive == 0:
        if just_switched == 0:
            hold_time = 0
            if GPIO.input(start_thik_ch) == 0:
                mode = 'thikka'
                drive = 1
            if GPIO.input(reverse_suste_ch) == 0:
                mode = 'reverse'
                drive = -1
        just_switched += 40
        if just_switched >= 800:
            just_switched = 0
    else:
        if veh_speed == 0:
            if GPIO.input(start_thik_ch) == 0:
                hold_time += 40
                mode = 'thikka'
                drive = 1
                if hold_time >=  1000:
                    mode = 'standby'
                    drive = 0
                    just_switched = 1
            if GPIO.input(start_thik_ch) == 1:
                hold_time = 0
    if drive == 1:
        if GPIO.input(reverse_suste_ch) == 0:
            mode = 'suste'
        if GPIO.input(babbal_ch) == 0:
            mode = 'babbal'
    
                
    gpio_data = {
        'hibeam': hibeam,
        'lturn': lturn,
        'rturn': rturn,
        'mode': mode,
        'drive': drive
    }
    return gpio_data
    
veh_speed = 0
while True:
    gpio_data = get_gpio(veh_speed)
    os.system('clear')
    print('Hi beam: ', gpio_data.get('hibeam','none'))
    print('Left turn: ', gpio_data.get('lturn','none'))
    print('Right turn: ', gpio_data.get('rturn','none'))
    print('Hi beam: ', gpio_data.get('hibeam','none'))
    print('Hi beam: ', gpio_data.get('hibeam','none'))
	

