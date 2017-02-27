import threading
from random import randint, choice
from time import sleep
import logging
from paramiko.client import SSHClient, AutoAddPolicy

logger = logging.getLogger(__name__)


class SSH(threading.Thread):

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.c = config

        # For delay range
        up, down = self.c['delay_range'].split('-')
        self.delay_range = (int(up), int(down))

        self.commands = self.c['commands'].split('\n')
        self.files = self.c['files'].split('\n')
        self.dirs = ['/'.join(file.split('/')[:-1]) for file in self.files]

    def run(self):
        logger.info("Starting SSH client")
        with SSHClient() as ssh:
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(hostname=self.c['host'],
                        username=self.c['login'],
                        password=self.c['pass'],
                        look_for_keys=False)
            logger.debug('SSH client connected')

            while True:
                # Pick command to send
                command = choice(self.commands)
                if '@f' in command:
                    command = command.replace('@f', choice(self.files))
                elif '@d' in command:
                    command = command.replace('@d', choice(self.dirs))

                logger.info('Executing command `{}`'.format(command))
                out = ssh.exec_command(command)
                logger.debug('Output: {}'.format(out))

                delay = randint(*self.delay_range)
                logger.debug('Waiting for {} seconds'.format(delay))
                sleep(delay)
