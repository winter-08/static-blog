import os
import shutil
import re
from html_markdown import markdown_to_html_node

def main():
    #__location__ = os.path.realpath(os.path.join(os.getcwd(), 'public'))
    __location__ = './public' 
    if os.path.exists(__location__):
        shutil.rmtree(__location__)
    #os.mkdir(__location__)
    #copy_files(os.path.join(os.getcwd(), 'static'))
    copy_files('./static', __location__)
    generate_page('./content/index.md', './template.html', 'public/index.html')

def copy_files(from_path: str, dest_path: str) -> None:
    if not os.path.exists(dest_path):
        print(f"creating path: {dest_path}")
        os.mkdir(dest_path)
    paths = os.listdir(from_path)
    for p in paths:
        full_path = os.path.join(from_path, p)
        if not os.path.isfile(full_path):
            copy_files(full_path, os.path.join(dest_path, p))
        else:
            print(f"copying file: {full_path}")
            shutil.copyfile(full_path, os.path.join(dest_path, p))

#def copy_files(path):
#    paths = os.listdir(path)
#    for p in paths:
#        full_path = os.path.join(path, p)
#        #print(os.path.isfile(full_path))
#        if not os.path.isfile(full_path):
#            print('Creating path')
#own>            os.mkdir(os.getcwd())
#        copy_files(p)
#        else:
#            print('copying file')
#            shutil.copyfile(full_path, os.path.join(os.getcwd(), 'public', os.path.relpath(full_path, os.path.join(os.getcwd(), 'static'))))
#    return

def extract_title(markdown: str) -> str:
    if not markdown.lstrip().startswith('# '):
        raise ValueError("Markdown to start with heading")
    match = re.match(r'^\s*#\s+(.+)', markdown)
    if match:
        return match.group(1).strip()
    raise ValueError("Markdown doesn't contain a valid title")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md:
        md_file = md.read()
        md.close()
    with open(template_path) as tmp:
        tmp_file = tmp.read()
        tmp.close()
    node = markdown_to_html_node(md_file)
    #print(f"length: {len(node.children)}")
    content = node.to_html()
    title = extract_title(md_file)
    print(title)
#    print(f"cnt: {content}")
    tmp_file = tmp_file.replace('{{ Title }}', title)
    tmp_file = tmp_file.replace('{{ Content }}', content)
    print(f"content: {tmp_file}")
    #print(f"test: {os.path.dirname(dest_path)}")
    os.makedirs(os.path.split(dest_path)[0], exist_ok=True)
    with open(dest_path, 'w+') as html_file:
        html_file.write(tmp_file)
        html_file.close()

if __name__ == "__main__":
    main()
