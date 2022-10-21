import  os
import  shutil
import  hashlib

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""
   # make a hash object
   h = hashlib.sha1()
   # open file for reading in binary mode
   with open(filename,'rb') as file:
       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)
   # return the hex representation of digest
   return h.hexdigest()

def check_forward(path_src,path_dst):

    print('Include ',os.listdir(path_src))


    #running through the dir
    for i in os.listdir(path_src):
        if os.path.isdir(path_src) and not i.startswith('.'):

            if not os.path.exists(path_dst):
                os.mkdir(path_dst)

            print('Go down '+path+'/'+i)
            check_forward(path_src+'/'+i,path_dst)
            print('return to',path)

        else:

            if not os.path.exists(path_dst+'/'+i):
                src_filename = path_src+'/'+i
                dst_filename = path_dst+'/'+i
                src_checksum = hash_file(src_filename)
                dst_checksum = hash_file(dst_filename)

                if src_checksum != dst_checksum:
                    shutil.copyfile(src_filename, dst_filename)
                    print(dst_filename,' Updated!')




if __name__ == '__main__':

    path = r'/Users/antonlipchansky/Desktop/test_dir'
    path_dest = r'/Users/antonlipchansky/Desktop/test_dir_dest'

    check_forward(path,path_dest)








