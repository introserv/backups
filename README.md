
# backups from https://intorserv.eu
Скрипт написан на Python2.5 - обычно установлен по умолчанию

Для запуска скрипта необходимо его скопировать на свой сервер:<br>
```
curl -O https://raw.githubusercontent.com/introserv/backups/master/backup2ftp.py
```

Сделать его исполняемым:<br>
```
chmod +x backup2ftp.py
```
И настроить параметры в начале скрипта:<br>
```python
FTP_URL = "ftp.domain" # настройки фтп сервера
FTP_DIR = "/"
FTP_USER = "user"
FTP_PASS = "pass"
MAX_BACKUPS_COUNT = 3 #количество сохраняемых копий на удаленном сервере
BACKUPS_DIR = "/"
BACKUPS_FILE_EXT = "tar" #расширение файлов, которые надо скопировать
OPENSSL_SALT = "pass" #пароль для шифрования файлов
ALARM_EMAIL_FROM = "email-from@domain" #от кого оповещение о результате копирования
ALARM_EMAIL_TO = "email-to@domain" #кому оповещение о результате копирования
SMTP_HOST = "domain:port" #настойки почтового сервера
SMTP_AUTH = True
SMTP_USER = "user"
SMTP_PASSWD = "pass"
```
Файлы копируются на удаленный сервер в зашифрованном виде с помощью openssl.
Чтобы расшифровать обратно надо запустить:
```
backup2ftp.py your_file
```
