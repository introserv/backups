#!/usr/bin/env python

import time
from ftplib import FTP
import os
import smtplib
from subprocess import Popen, PIPE
from hashlib import sha256
from os import SEEK_END
import sys


#######################
# Config section
FTP_URL = "ftp.domain"
FTP_DIR = "_____"
FTP_USER = "_____"
FTP_PASS = "_____"
MAX_BACKUPS_COUNT = 3
BACKUPS_DIR = "/_____"
BACKUPS_FILE_EXT = "tar"
OPENSSL_SALT = "_____"
ALARM_EMAIL_FROM = "_____"
ALARM_EMAIL_TO = "_____"
SMTP_HOST = "domain:port"
SMTP_AUTH = True
SMTP_USER = "_____"
SMTP_PASSWD = "_____"
#######################


class EncryptionError(Exception):
    pass


def list_ftp_dir(ftp):
    return ftp.nlst()


def test_files_count(ftp):
    ls = list_ftp_dir(ftp)
    user_files = dict()
    for i in ls:
        if i.endswith("."+BACKUPS_FILE_EXT+".enc"):
            usr = i.split(".")[0]
            if user_files.get(usr) is None:
                user_files[usr] = []
            user_files[usr].append(i)

    for f in user_files:
        fs = user_files[f]
        if len(fs) > MAX_BACKUPS_COUNT:
            print("DEL User files ", f)
            sorted(fs)
            for fd in fs[:-MAX_BACKUPS_COUNT]:
                print("DEL ", fd)
                ftp.delete(fd)


def file_hash(pth):
    """
    Calculate the checksum of a file; return length-40 binary that includes the algorithm.
    """
    shaer = sha256()
    with open(pth, 'rb') as fh:
        data = ' '
        while data:
            data = fh.read(32768)
            shaer.update(data)
    return b'sha256__' + shaer.digest()


def encrypt_file(rawpth, key, encpth=None):
    """
    Use openssl to encrypt a file using `aes-256` with a salt (no key stretching implicit).
    """
    if encpth is None:
        encpth = '{0:s}.enc'.format(rawpth)
    proc = Popen([
        'openssl', 'aes-256-cbc', '-salt',
        '-in', rawpth, '-out', encpth,
        '-e', '-k', '{0:s}'.format(key),
    ], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if err:
        raise EncryptionError('encrypting "{0:s}" failed due to openssl error:\n"{1:s}"'
            .format(rawpth, err.decode('ascii').strip()))
    checksum = file_hash(rawpth)
    with open(encpth, 'ab') as fh:
        fh.write(b'Checksum_' + checksum)

    return encpth


def decrypt_file(encpth, key, rawpth=None):
    """
    Reverse of `encrypt_file`.
    """
    if rawpth is None:
        rawpth = encpth
        if rawpth.endswith('.enc'):
            rawpth = rawpth[:-4]
    with open(encpth, 'rb') as fh:
        fh.seek(-49, SEEK_END)
        if not fh.read(9) == b'Checksum_':
            raise EncryptionError('no checksum found at the end of "{0:s}"'.format(encpth))
        checksum_found = fh.read()
    with open(encpth, 'ab') as fh:
        fh.seek(-49, SEEK_END)
        fh.truncate()
    proc = Popen([
        'openssl', 'aes-256-cbc', '-salt',
        '-in', encpth, '-out', rawpth,
        '-d', '-k', '{0:s}'.format(key),
    ], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    with open(encpth, 'ab') as fh:
        fh.seek(0, SEEK_END)
        fh.write(b'Checksum_' + checksum_found)
    if err:
        raise EncryptionError('decrypting "{0:s}" failed due to openssl error:\n"{1:s}"'
            .format(encpth, err.decode('ascii').strip()))
    checksum_decrypted = file_hash(rawpth)
    if not checksum_found == checksum_decrypted:
        raise EncryptionError('The decrypted file does not have the same checksum as the original!\n' +
            ' original:  {0:}\n decrypted: {1:}\n'.format(checksum_found, checksum_decrypted))
    return rawpth


def upload_files(ftp):
    ls = [_[:-4] for _ in list_ftp_dir(ftp)]
    for fname in os.listdir(BACKUPS_DIR):
        if fname.endswith("."+BACKUPS_FILE_EXT) and fname not in ls:
            print("Upload - ", fname)
            encrypt_file(os.path.join(BACKUPS_DIR, fname), OPENSSL_SALT)
            with open(os.path.join(BACKUPS_DIR, fname + ".enc"), 'rb') as fobj:
                ftp.storbinary('STOR ' + fname + ".enc", fobj, 2048)
            os.remove(os.path.join(BACKUPS_DIR, fname + ".enc"))
        else:
            print("Skip - ", fname)


def send_mail(subj, text):

    SUBJECT = subj

    BODY = "\r\n".join((
        "From: %s" % ALARM_EMAIL_FROM,
        "To: %s" % ALARM_EMAIL_TO,
        "Subject: %s" % SUBJECT,
        "",
        text
    ))
    try:
        server = smtplib.SMTP_SSL(SMTP_HOST)
        if SMTP_AUTH:
            server.login(SMTP_USER, SMTP_PASSWD)
        server.sendmail(ALARM_EMAIL_FROM, [ALARM_EMAIL_TO], BODY)
        server.quit()
    except Exception as e:
        print("Ooops - " + str(e))


def main():
    start_time = time.time()
    try:
        ftp = FTP()
        ftp.connect(host=FTP_URL)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)

        ftp.cwd(FTP_DIR)
        upload_files(ftp)
        test_files_count(ftp)

        ftp.quit()
    except Exception as e:
        send_mail("Backup failed", str(e))
    else:
        send_mail("Backup success", "All ok")
    end_time = time.time()

    print("Remote backup complited {} sec".format(end_time - start_time))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        try:
            decrypt_file(fn, OPENSSL_SALT)
        except Exception as e:
            print(str(e))
    else:
        main()
