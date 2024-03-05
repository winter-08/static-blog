from htmlnode import HTMLNode, LeafNode


text_types = {
    "text_type_text": "text",
    "text_type_bold": "bold",
    "text_type_italic": "italic",
    "text_type_code": "code",
    "text_type_link": "link",
    "text_type_image": "image",
}


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, compNode) -> bool:
        if self.text is not compNode.text:
            return False
        if self.text_type is not compNode.text_type:
            return False
        if self.url is not compNode.url:
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

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    pass
