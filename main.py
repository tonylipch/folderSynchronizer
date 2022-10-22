import os
import shutil
import hashlib
import schedule
import  time
import logging

logging.basicConfig(filename="operations.log", level=logging.INFO)


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
                    print(dst_filename, ' Created!')
                    logging.info(str(dst_filename)+': Created!')

                check_forward(src_filename, dst_filename)

        else:

            if not os.path.exists(dst_filename):
                shutil.copyfile(src_filename, dst_filename)
                print(dst_filename, ' Copied!')
                logging.info(str(dst_filename) +': Copied!')
            else:
                src_checksum = hash_file(src_filename)
                dst_checksum = hash_file(dst_filename)

                if src_checksum != dst_checksum:
                    shutil.copyfile(src_filename, dst_filename)
                    print(dst_filename, 'Updated!')
                    logging.info(str(dst_filename)+': file Updated')



def remove_recursively(path):
    if os.path.isdir(path):
        for i in os.listdir(path):
            remove_recursively(path + '/' + i)
        os.rmdir(path)
    else:
        os.remove(path)
    print(path, 'Removed')
    logging.info(str(path)+': file Removed!')


def check_backward(path_src, path_dst):


    for i in os.listdir(path_dst):
        src_filename = path_src + '/' + i
        dst_filename = path_dst + '/' + i
        if not os.path.exists(src_filename):
            remove_recursively(dst_filename)
        else:
            if os.path.isdir(dst_filename):
                check_backward(src_filename, dst_filename)






if __name__ == '__main__':
    path_src =  r'Enter source directory'
    path_dest = r'Enter replica directory'

    schedule.every().hour.do(check_forward,path_src,path_dest)
    schedule.every().hour.do(check_backward,path_src,path_dest)

    while True:
        schedule.run_pending()
        time.sleep(1)











