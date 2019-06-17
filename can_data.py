import can
import time
import os

# Set can parameters and create 'bus' object
can.rc['interface'] = 'socketcan_native'
can.rc['channel'] = 'can0'

# Initialize variables
bat_current = 0
bat_voltage = 0
veh_speed = 0
max_torque = 0
torque_act = 0
motor_temp = 0
motor_vel = 0
drive_prof = 0
trip_dist = 0
htsink_temp = 0
dig_input = 0

while True:    
    # Get data
    bus = can.interface.Bus()
    message = bus.recv(0.0)

    # Filter data
    if (message != None):
        if (message.arbitration_id!=128):
            if (message.arbitration_id==663):   # TPDO 3: Battery Parameters
                # Perform data swap in binary
                data = message.data
                new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]

                # Convert new_data to hex
                count = 0
                for d in new_data:
                    d_hex = hex(d)[2:]
                    new_data[count] = d_hex
                    count += 1
                    
                bat_current_hex = new_data[0] + new_data[1]
                bat_voltage_hex = new_data[4] + new_data[5]

                bat_current = int(bat_current_hex, 16)*0.0625
                bat_voltage = int(bat_voltage_hex, 16)*0.0625

            if (message.arbitration_id==768):
                # Perform data swap in binary
                data = message.data
                new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]

                # Convert new_data to hex
                count = 0
                for d in new_data:
                    d_hex = hex(d)[2:]
                    new_data[count] = d_hex
                    count += 1
                    
                veh_speed_hex = new_data[0] + new_data[1]
                max_torque_hex = new_data[2] + new_data[3]
                torque_act_hex = new_data[4] + new_data[5]
                motor_temp_hex = new_data[6] + new_data[7]

                veh_speed = int(veh_speed_hex, 16)*0.0625
                max_torque = int(max_torque_hex, 16)*0.1
                torque_act = int(torque_act_hex, 16)*0.0625
                motor_temp = int(motor_temp_hex, 16)*1

            if (message.arbitration_id==336):
                # Perform data swap in binary
                data = message.data
                new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]

                # Convert new_data to hex
                count = 0
                for d in new_data:
                    d_hex = hex(d)[2:]
                    new_data[count] = d_hex
                    count += 1
                    
                motor_vel_hex = new_data[6] + new_data[7] + new_data[4] + new_data[5]
                motor_vel = int(motor_vel_hex, 16)*1

            if (message.arbitration_id==664):
                # Perform data swap in binary
                data = message.data
                new_data = [data[1], data[0], data[3], data[2]]

                # Convert new_data to hex
                count = 0
                for d in new_data:
                    d_hex = hex(d)[2:]
                    new_data[count] = d_hex
                    count += 1
                    
                drive_prof_hex = new_data[0] + new_data[1]
                drive_prof = int(drive_prof_hex, 16)*1

            if (message.arbitration_id==769):
                # Perform data swap in binary
                data = message.data
                new_data = [data[1], data[0], data[3], data[2], data[5], data[4], data[7], data[6]]

                # Convert new_data to hex
                count = 0
                for d in new_data:
                    d_hex = hex(d)[2:]
                    new_data[count] = d_hex
                    count += 1
                    
                trip_dist_hex = new_data[2] + new_data[3] + new_data[0] + new_data[1]
                htsink_temp_hex = new_data[7]
                dig_input_hex = new_data[6]

                trip_dist = int(trip_dist_hex, 16)*0.0039
                htsink_temp = int(htsink_temp_hex, 16)*1
                dig_input = int(dig_input_hex, 16)*1
            
            '''
            
            # Print stuff
            os.system('clear')
            print('Battery Current: ', bat_current, ' A')
            print('Battery Voltage: ', bat_voltage, ' V')
            print('Vehicle Speed: ', veh_speed, ' km/h')
            print('Max Torque: ', max_torque, ' %')
            print('Actual Torque: ', torque_act, ' Nm')
            print('Motor Temperature: ', motor_temp, ' deg C')
            print('Velocity: ', motor_vel, ' rpm')
            print('Drive profile: ', drive_prof)
            print('Trip distance: ', trip_dist, ' km')
            print('Heat sink temp: ', htsink_temp, 'deg C')
            print('Digital input: ', dig_input)
            
            #time.sleep(0.001)
            
            '''
            
    


