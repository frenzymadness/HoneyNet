import threading
from random import randint, choice
from time import sleep
import logging
import ftplib
from ftplib import FTP as FTPConnection
import os
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)


def print_to_null(s):
    with open(os.devnull, 'w') as fh:
        print(s, file=fh)


class FTP(threading.Thread):

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.c = config

        # For delay range
        up, down = self.c['delay_range'].split('-')
        self.delay_range = (int(up), int(down))

        # For file size range
        up, down = self.c['file_size_range'].split('-')
        self.file_size_range = (int(up), int(down))

    def run(self):
        logger.info("Starting FTP client")
        with FTPConnection(self.c['host'], self.c['login'], self.c['pass']) as ftp:

            ftp.cwd(self.c['folder'])
            logger.debug('Switched to {} folder'.format(self.c['folder']))

            files_list = ftp.nlst()
            logger.info('File list extended with {} files'.format(len(files_list)))

            while True:

                action = choice(['read', 'write'])

                if action == 'read' and files_list:
                    file = choice(files_list)
                    logger.debug('Performing "read" action with {} file'.format(file))
                    try:
                        ftp.retrbinary("RETR " + file, print_to_null)
                    except ftplib.error_perm:
                        logger.error('Permision error occured during RETR action')
                elif action == 'write':
                    with NamedTemporaryFile() as file:
                        # Generate random file size
                        file_size = randint(*self.file_size_range)
                        logger.debug('Performing "write" action with {} file {} MB size'.format(file.name, file_size))
                        # Write file full of random data
                        file.write(os.urandom(1024 * 1024 * file_size))
                        file.seek(0)
                        # Upload file to FTP
                        file_name = file.name.split('/')[-1]
                        ftp.storbinary('STOR ' + file_name, file)
                        # Append new file to files_list
                        files_list.append(file_name)
                        files_list = list(set(files_list))

                delay = randint(*self.delay_range)
                logger.debug('Waiting for {} seconds'.format(delay))
                sleep(delay)
