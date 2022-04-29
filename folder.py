import os


def folder(parent_dir,directory):
    
    path = os.path.join(parent_dir,directory)
    if os.path.isdir(path):
        return path
    os.mkdir(path)
    print (f'Directory {directory} created')
    return path



