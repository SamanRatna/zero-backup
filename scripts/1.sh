ip link set can0 up type can bitrate 500000 &
# sudo btmgmt -i hci0 bredr off
# sudo btmgmt -i hci0 le on
pon &
cd /home/pi/yatri-project-zero/vehicle_manager
python3 vm_main.py
