import RPi.GPIO as GPIO
import time
import os

# Set GPIO pin definition
GPIO.setmode(GPIO.BCM)

hibeam_in = 2
lturn_in = 3
rturn_in = 4
lsig_in = 10
rsig_in = 9
start_thik_in = 17
reverse_suste_in = 27
babbal_in = 22
stand_in = 25
start_thik_out = 14
suste_out = 18
reverse_out = 15
babbal_out = 23
charge_out = 24
start_out = 8
lturn_out = 7
rturn_out = 12

GPIO.setup(hibeam_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lturn_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rturn_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_thik_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reverse_suste_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(babbal_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stand_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lsig_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rsig_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(start_thik_out, GPIO.OUT)
GPIO.setup(suste_out, GPIO.OUT)
GPIO.setup(reverse_out, GPIO.OUT)
GPIO.setup(babbal_out, GPIO.OUT)
GPIO.setup(charge_out, GPIO.OUT)
GPIO.setup(start_out, GPIO.OUT)
GPIO.setup(lturn_out, GPIO.OUT)
GPIO.setup(rturn_out, GPIO.OUT)

GPIO.output(start_thik_out, GPIO.LOW)
GPIO.output(suste_out, GPIO.LOW)
GPIO.output(reverse_out, GPIO.LOW)
GPIO.output(babbal_out, GPIO.LOW)

# Assuming tail light input is active low:
GPIO.output(charge_out, GPIO.HIGH)
GPIO.output(start_out, GPIO.HIGH)
GPIO.output(lturn_out, GPIO.HIGH)
GPIO.output(rturn_out, GPIO.HIGH)

hibeam = 0
lturn = 0
rturn = 0
lsig_now = 0
rsig_now = 0
lsig_last = 0
rsig_last = 0
l_count = 0
r_count = 0
tlturn = 0
trturn = 0
mode = 'standby'
drive = 0
hold_time = 0
just_switched = 0

def get_gpio(veh_speed):
    global hibeam
    global lturn
    global rturn
    global lsig_now
    global rsig_now
    global lsig_last
    global rsig_last
    global l_count
    global r_count
    global tlturn
    global trturn
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
    
    lsig_now = GPIO.input(lturn_in) 
    rsig_now = GPIO.input(rturn_in) 
    
    if lsig_now-lsig_last == -1:
        tlturn = 1
        l_count = 0
    if lsig_now-lsig_last == 0:
        l_count += 6
        if l_count > 800:
            tlturn = 0
            l_count = 0
    if rsig_now-rsig_last == -1:
        trturn = 1
        r_count = 0
    if rsig_now-rsig_last == 0:
        r_count += 6
        if r_count > 800:
            trturn = 0
            r_count = 0
    
    lsig_last = GPIO.input(lturn_in)
    rsig_last = GPIO.input(rturn_in)

    if GPIO.input(stand_in) == 0:
        stand = 'down'
    else:
        stand = 'up'
    
    if stand == 'down':
        mode = 'standby'
        drive = 0
    else:
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
        'drive': drive,
        'stand': stand
    }
    return gpio_data
    
    
# Send ignition pulse to tail light
GPIO.output(start_out, GPIO.LOW)
time.sleep(0.2)
GPIO.output(start_out, GPIO.HIGH)

# Run infinite loop for remaining signals
veh_speed = 0
lturn_count = 0
rturn_count = 0

while True:
    start = time.time()
    gpio_data = get_gpio(veh_speed)
    os.system('clear')
    print('Hi beam: ', gpio_data.get('hibeam','none'))
    print('Left turn: ', gpio_data.get('lturn','none'))
    print('Right turn: ', gpio_data.get('rturn','none'))
    print('Tail Left: ', tlturn)
    print('Tail Right: ', trturn)
    print('Mode: ', gpio_data.get('mode','none'))
    print('Stand: ', gpio_data.get('stand','none'))
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
    
    if tlturn == 1 and trturn == 1:
        GPIO.output(lturn_out, GPIO.HIGH)
        GPIO.output(rturn_out, GPIO.HIGH)
    else:
        if tlturn == 1:
            GPIO.output(lturn_out, GPIO.LOW)
        else:
            GPIO.output(lturn_out, GPIO.HIGH)    
        if trturn == 1:
            GPIO.output(rturn_out, GPIO.LOW)
        else:
            GPIO.output(rturn_out, GPIO.HIGH)
        
    end = time.time()
    print('Time taken: ', end-start, 'seconds')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
	

