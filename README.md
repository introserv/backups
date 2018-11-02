
# backups from https://intorserv.eu
Скрипт написан на Python2.5 - обычно установлен по умолчанию

Для запуска скрипта необходимо его скопировать на свой сервер:
curl -O https://raw.githubusercontent.com/introserv/backups/master/backup2ftp.py

Сделать его исполняемым:
chmod +x backup2ftp.py

И настроить параметры в начале скрипта:

FTP_URL = "ftp.domain" - настройки фтп сервера
FTP_DIR = "_____"
FTP_USER = "_____"
FTP_PASS = "_____"
MAX_BACKUPS_COUNT = 3 - количество сохраняемых копий на удаленном сервере
BACKUPS_DIR = "/_____"
BACKUPS_FILE_EXT = "tar" - расширение файлов, которые надо скопировать
OPENSSL_SALT = "_____" - пароль для шифрования файлов
ALARM_EMAIL_FROM = "_____" - от кого оповещение о результате копирования
ALARM_EMAIL_TO = "_____" - кому оповещение о результате копирования
SMTP_HOST = "domain:port" - настойки почтового сервера
SMTP_AUTH = True
SMTP_USER = "_____"
SMTP_PASSWD = "_____"

Файлы копируются на удаленный сервер в зашифрованном виде с помощью openssl
Чтобы расшифровать обратно надо запустить:
backup2ftp.py your_file
