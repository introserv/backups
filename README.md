
# backups from https://intorserv.eu
Скрипт написан на Python2.5 - обычно установлен по умолчанию

Для запуска скрипта необходимо его скопировать на свой сервер:<br>
curl -O https://raw.githubusercontent.com/introserv/backups/master/backup2ftp.py

Сделать его исполняемым:<br>
chmod +x backup2ftp.py

И настроить параметры в начале скрипта:<br>

FTP_URL = "ftp.domain" - настройки фтп сервера<br>
FTP_DIR = "/"<br>
FTP_USER = "user"<br>
FTP_PASS = "pass"<br>
MAX_BACKUPS_COUNT = 3 - количество сохраняемых копий на удаленном сервере<br>
BACKUPS_DIR = "/"<br>
BACKUPS_FILE_EXT = "tar" - расширение файлов, которые надо скопировать<br>
OPENSSL_SALT = "pass" - пароль для шифрования файлов<br>
ALARM_EMAIL_FROM = "email-from@domain" - от кого оповещение о результате копирования<br>
ALARM_EMAIL_TO = "email-to@domain" - кому оповещение о результате копирования<br>
SMTP_HOST = "domain:port" - настойки почтового сервера<br>
SMTP_AUTH = True<br>
SMTP_USER = "user"<br>
SMTP_PASSWD = "pass"<br>

Файлы копируются на удаленный сервер в зашифрованном виде с помощью openssl<br>
Чтобы расшифровать обратно надо запустить:<br>
backup2ftp.py your_file
