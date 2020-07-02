import socket
import keyboard
import time
import json
import sys
from io import StringIO

not_connected = False

print("\n".join(sys.argv))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(bytes(json.dumps({"timestamp": time.time(), "name": 'Andi'}), "utf-8"), ('172.16.17.80', 1111))
position = 300

# while not_connected:
#    s.sendto(bytes(json.dumps({"timestamp": time.time(), "name": 'Andi'}), "utf-8"), ('172.16.17.80', 1111))
#    jsonMsg, address = s.recvfrom(1024)
#    msg = json.load(StringIO(jsonMsg.decode("utf-8")))
#    if msg['connected']:
#        not_connected = False

while True:
    if keyboard.is_pressed("w") or keyboard.is_pressed("a") or keyboard.is_pressed("up arrow") or keyboard.is_pressed("left arrow"):
        position -= 10
    if keyboard.is_pressed("s") or keyboard.is_pressed("d") or keyboard.is_pressed("down arrow") or keyboard.is_pressed("right arrow"):
        position += 10
    if position < 0:
        position = 0
    elif position > 600:
        position = 600
    s.sendto(bytes(json.dumps({"timestamp": time.time(), "position": position}), "utf-8"), ('172.16.17.80', 1111))
    time.sleep(1/60)
