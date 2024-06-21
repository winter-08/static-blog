#from textnode import TextNode
import os
import shutil

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), 'public'))
    if os.path.exists(__location__):
        shutil.rmtree(__location__)
    os.mkdir(__location__)
    copy_files(os.path.join(os.getcwd(), 'static'))

def copy_files(path):
    paths = os.listdir(path)
    for p in paths:
        print(p)
        full_path = os.path.join(path, p)
        print(os.path.isfile(full_path))
        if not os.path.isfile(full_path):
            print('Creating path')
            os.mkdir(os.getcwd())
            copy_files(p)
        else:
            print('copying file')
            shutil.copyfile(full_path, os.path.join(os.getcwd(), 'public', os.path.relpath(full_path, os.path.join(os.getcwd(), 'static'))))
    return

if __name__ == "__main__":
    main()
