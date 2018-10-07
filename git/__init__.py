import logging
import os
import subprocess
import tarfile
from distutils.spawn import find_executable

from .exceptions import GitExecutionError

__author__ = 'Jacopo Scrinzi'
__version__ = '0.0.1'

logging.basicConfig()
LOGGER = logging.getLogger('git')
LOGGER.setLevel(logging.INFO)

PKG_PATH = os.path.dirname(os.path.realpath(__file__))
VENDOR_PATH = os.path.realpath('{}/../vendor'.format(PKG_PATH))
GIT_VERSION = '2.4.3'
GIT_TAR_FILE = '{}/git-{}.tar'.format(VENDOR_PATH, GIT_VERSION)
TMP_PATH = '/tmp'
BIN_PATH = os.path.join(TMP_PATH, 'usr/bin')
GIT_TEMPLATE_DIR = os.path.join(TMP_PATH, 'usr/share/git-core/templates')
GIT_EXEC_PATH = os.path.join(TMP_PATH, 'usr/libexec/git-core')
LD_LIBRARY_PATH = os.path.join(TMP_PATH, 'usr/lib64')
GIT_BINARY = '{}/usr/bin/git'.format(TMP_PATH)


if not find_executable('git'):
    LOGGER.info('git not found installing using local copy')
    if not os.path.isfile(GIT_BINARY):
        LOGGER.info('extracting git tarball')
        tar = tarfile.open(GIT_TAR_FILE)
        tar.extractall(path=TMP_PATH)
        tar.close()

    LOGGER.info('setting up environment variables')
    os.environ['PATH'] += ':{}'.format(BIN_PATH)
    os.environ['GIT_TEMPLATE_DIR'] = GIT_TEMPLATE_DIR
    os.environ['GIT_EXEC_PATH'] = GIT_EXEC_PATH
    os.environ['LD_LIBRARY_PATH'] = LD_LIBRARY_PATH


def exec_command(args, cwd='/tmp', env=os.environ):
    command = ['git'] + args
    LOGGER.info('executing git command: "{}"'.format(' '.join(command)))
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, cwd=cwd, env=env)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        LOGGER.error('git failed with {} returncode'.format(p.returncode))
        raise GitExecutionError(
            'command={} returncode={} stdout="{}" '
            'stderr="{}"'.format(command, p.returncode, stdout, stderr)
        )
    return stdout, stderr