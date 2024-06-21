#from textnode import TextNode
import os
import shutil
import re

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

def extract_title(markdown: str) -> str:
    if not markdown.lstrip.startswith('# '):
        raise ValueError("Markdown to start with heading")
    match = re.match(r'^\s*#\s+(.+)', markdown)
    if match:
        return match.group(1).strip()
    raise ValueError("Markdown doesn't contain a valid title")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    pass

if __name__ == "__main__":
    main()
