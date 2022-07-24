# Author: Manas Bhatt
# Contact: manas.bh4tt@gmail.com
# Date : Jun 2022

import os
import shutil

def createDirectory(path, name):
    dirPath = path + "\\" + name
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

#recursive move the files/sub directories to new directory
#delete the destdir files keeping dir tree structure
def moveFiles(srcdir, destdir):
    try:
        dest = shutil.copytree(srcdir, destdir)
    except FileExistsError:
        shutil.rmtree(destdir)
        dest = shutil.copytree(srcdir, destdir)
    except:
        return "Error generated"
    
    for root, dirs, files in os.walk(srcdir):
        for file in files:
            os.remove(os.path.join(root, file))

    return "Files Archived"

    
