import re
from htmlnode import HTMLNode, LeafNode


text_types = {
    "text_type_text": "text",
    "text_type_bold": "bold",
    "text_type_italic": "italic",
    "text_type_code": "code",
    "text_type_link": "link",
    "text_type_image": "image",
}

valid_text_types = {
    "text_type_text": "text",
    "text_type_bold": "bold",
    "text_type_italic": "italic",
    "text_type_code": "code",
    "text_type_underline": "underline"
}


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, compNode) -> bool:
        if self.text != compNode.text:
            return False
        if self.text_type != compNode.text_type:
            return False
        if self.url != compNode.url:
            return False
        return True

    def __repr__(self) -> str:
        return f"TextNode('{self.text}', '{self.text_type}', '{self.url}')"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type not in text_types:
        raise ValueError(
            f"Invalid text_type: {text_node.text_type}. Valid types are: {', '.join(text_types.keys())}"
        )

    node_mappings = {
        "text": lambda: LeafNode(value=text_node.text),
        "bold": lambda: LeafNode(tag="b", value=text_node.text),
        "italic": lambda: HTMLNode(tag="i", value=text_node.text),
        "code": lambda: HTMLNode(tag="code", value=text_node.text),
        "link": lambda: HTMLNode(
            tag="a",
            value=text_node.text,
            props={"href": text_node.url, "target": "_blank"},
        ),
        "image": lambda: HTMLNode(
            tag="img", props={"src": text_node.url, "alt": text_node.text}
        ),
    }

    return node_mappings[text_node.text_type]()

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list:
    split_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != "text":
            split_nodes.append(node)
            continue
        if delimiter not in node.text:
            raise ValueError('Delimiter not found')
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError('Closing delimiter not found')
        for i in range(len(split_node)):
            if i % 2 == 0:
                if split_node[i]:
                    split_nodes.append(TextNode(split_node[i], "text"))
            else:
                split_nodes.append(TextNode(split_node[i], text_type))
    return split_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    image_pattern = r"!\[(?P<alt>.*?)\]\((?P<link>.*?)\)"
    matches = re.findall(image_pattern, text)
    return [(alt, link) for alt, link in matches]

def extract_markdown_links(text: str) -> list[tuple]:
    link_pattern = r"\[(?P<text>.*?)\]\((?P<url>.*?)\)"
    matches = re.findall(link_pattern, text)
    return [(text, url) for text, url in matches]
