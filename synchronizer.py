import os
import shutil
import hashlib
import time
import logging
from datetime import datetime
import sys

import pycron as pycron

file_log = logging.FileHandler('Log.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)


def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""
    # make a hash object
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    # return the hex representation of digest
    return h.hexdigest()


def check_forward(path_src, path_dst):
    for i in os.listdir(path_src):
        src_filename = path_src + '/' + i
        dst_filename = path_dst + '/' + i
        if os.path.isdir(src_filename):
            if not i.startswith('.'):
                if not os.path.exists(dst_filename):
                    os.mkdir(dst_filename)
                    logging.info(str(dst_filename) + ': Created!')

                check_forward(src_filename, dst_filename)

        else:

            if not os.path.exists(dst_filename):
                shutil.copyfile(src_filename, dst_filename)
                logging.info(str(dst_filename) + ': Copied!')
            else:
                src_checksum = hash_file(src_filename)
                dst_checksum = hash_file(dst_filename)

                if src_checksum != dst_checksum:
                    shutil.copyfile(src_filename, dst_filename)
                    logging.info(str(dst_filename) + ': file Updated')


def remove_recursively(path):
    if os.path.isdir(path):
        for i in os.listdir(path):
            remove_recursively(path + '/' + i)
        os.rmdir(path)
    else:
        os.remove(path)
    logging.info(str(path) + ': file Removed!')


def check_backward(path_src, path_dst):
    for i in os.listdir(path_dst):
        src_filename = path_src + '/' + i
        dst_filename = path_dst + '/' + i
        if not os.path.exists(src_filename):
            remove_recursively(dst_filename)
        else:
            if os.path.isdir(dst_filename):
                check_backward(src_filename, dst_filename)


def synchronize(src, dst):

    check_forward(src, dst)
    check_backward(src, dst)



if __name__ == '__main__':
    path_src = ""
    path_dest = ""
    pycron_time = ""


    if len(sys.argv) != 4:
        logging.error("error. use:\nsync <src-dir> <dst-dit> \"<cron expr>\"")
        exit(0)
    else:
        path_src = sys.argv[1]
        path_dest = sys.argv[2]
        pycron_time = sys.argv[3]


    while True:
        if pycron.is_now(pycron_time):
            synchronize(path_src, path_dest)
