import socket
import keyboard
import time
import json
import sys

not_connected = False
ip = "172.16.17.220"
port = 2222

print("\n".join(sys.argv))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(bytes(json.dumps({"timestamp": time.time(), "name": 'Andi'}), "utf-8"), (ip, port))
position = 300

while True:
    if keyboard.is_pressed("w") or keyboard.is_pressed("a") or keyboard.is_pressed("up arrow") or keyboard.is_pressed("left arrow"):
        position -= 20
    if keyboard.is_pressed("s") or keyboard.is_pressed("d") or keyboard.is_pressed("down arrow") or keyboard.is_pressed("right arrow"):
        position += 20
    if position < 0:
        position = 0
    elif position > 600:
        position = 600
    s.sendto(bytes(json.dumps({"timestamp": time.time(), "position": position}), "utf-8"), (ip, port))
    time.sleep(1/60)
