import RPi.GPIO as GPIO
import time
import os

# Set GPIO pin definition
GPIO.setmode(GPIO.BCM)

hibeam_in = 2
lturn_in = 3
rturn_in = 4
start_thik_in = 17
reverse_suste_in = 27
babbal_in = 22
start_thik_out = 14
suste_out = 18
reverse_out = 15
babbal_out = 23

GPIO.setup(hibeam_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lturn_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rturn_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_thik_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reverse_suste_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(babbal_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(start_thik_out, GPIO.OUT)
GPIO.setup(suste_out, GPIO.OUT)
GPIO.setup(reverse_out, GPIO.OUT)
GPIO.setup(babbal_out, GPIO.OUT)

GPIO.output(start_thik_out, GPIO.LOW)
GPIO.output(suste_out, GPIO.LOW)
GPIO.output(reverse_out, GPIO.LOW)
GPIO.output(babbal_out, GPIO.LOW)

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
    
    if GPIO.input(hibeam_in) == 0:
        hibeam = 1
    else:
        hibeam = 0
    if GPIO.input(lturn_in) == 0:
        lturn = 1
    else:
        lturn = 0
    if GPIO.input(rturn_in) == 0:
        rturn = 1
    else:
        rturn = 0
        
    if drive == 0:
        if just_switched == 0:
            hold_time = 0
            if GPIO.input(start_thik_in) == 0:
                mode = 'thikka'
                drive = 1
            if GPIO.input(reverse_suste_in) == 0:
                mode = 'reverse'
                drive = -1
        just_switched += 8
        if just_switched >= 800:
            just_switched = 0
    else:
        if veh_speed == 0:
            if GPIO.input(start_thik_in) == 0:
                hold_time += 8
                mode = 'thikka'
                drive = 1
                if hold_time >=  1000:
                    mode = 'standby'
                    drive = 0
                    just_switched = 1
            if GPIO.input(start_thik_in) == 1:
                hold_time = 0
    if drive == 1:
        if GPIO.input(reverse_suste_in) == 0:
            mode = 'suste'
        if GPIO.input(babbal_in) == 0:
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
    start = time.time()
    gpio_data = get_gpio(veh_speed)
    os.system('clear')
    print('Hi beam: ', gpio_data.get('hibeam','none'))
    print('Left turn: ', gpio_data.get('lturn','none'))
    print('Right turn: ', gpio_data.get('rturn','none'))
    print('Mode: ', gpio_data.get('mode','none'))
    print(' ')
    if mode == 'thikka':
        GPIO.output(start_thik_out, GPIO.HIGH)
        GPIO.output(suste_out, GPIO.LOW)
        GPIO.output(reverse_out, GPIO.LOW)
        GPIO.output(babbal_out, GPIO.LOW)
        print('Thikka  ', GPIO.input(start_thik_out))
        print('Suste   ', GPIO.input(suste_out))
        print('Reverse ', GPIO.input(reverse_out))
        print('Babbal  ', GPIO.input(babbal_out))
    if mode == 'suste':
        GPIO.output(start_thik_out, GPIO.HIGH)
        GPIO.output(suste_out, GPIO.HIGH)
        GPIO.output(reverse_out, GPIO.LOW)
        GPIO.output(babbal_out, GPIO.LOW)
        print('Thikka  ', GPIO.input(start_thik_out))
        print('Suste   ', GPIO.input(suste_out))
        print('Reverse ', GPIO.input(reverse_out))
        print('Babbal  ', GPIO.input(babbal_out))
    if mode == 'babbal':
        GPIO.output(start_thik_out, GPIO.HIGH)
        GPIO.output(suste_out, GPIO.LOW)
        GPIO.output(reverse_out, GPIO.LOW)
        GPIO.output(babbal_out, GPIO.HIGH)
        print('Thikka  ', GPIO.input(start_thik_out))
        print('Suste   ', GPIO.input(suste_out))
        print('Reverse ', GPIO.input(reverse_out))
        print('Babbal  ', GPIO.input(babbal_out))
    if mode == 'reverse':
        GPIO.output(start_thik_out, GPIO.LOW)
        GPIO.output(suste_out, GPIO.LOW)
        GPIO.output(reverse_out, GPIO.HIGH)
        GPIO.output(babbal_out, GPIO.LOW)
        print('Thikka  ', GPIO.input(start_thik_out))
        print('Suste   ', GPIO.input(suste_out))
        print('Reverse ', GPIO.input(reverse_out))
        print('Babbal  ', GPIO.input(babbal_out))
    if mode == 'standby':
        GPIO.output(start_thik_out, GPIO.LOW)
        GPIO.output(suste_out, GPIO.LOW)
        GPIO.output(reverse_out, GPIO.LOW)
        GPIO.output(babbal_out, GPIO.LOW)
        print('Thikka  ', GPIO.input(start_thik_out))
        print('Suste   ', GPIO.input(suste_out))
        print('Reverse ', GPIO.input(reverse_out))
        print('Babbal  ', GPIO.input(babbal_out))
    end = time.time()
    print('Time taken: ', end-start, 'seconds')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
	

