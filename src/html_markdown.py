import re

from htmlnode import HTMLNode, ParentNode
from textnode import text_to_textnodes, text_node_to_html_node


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    blocks = [item.strip() for item in blocks if item.strip() and item != ""]
    return blocks


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def block_to_block_type(text: str) -> str:
    if is_markdown_heading_block(text):
        return block_type_heading
    if is_markdown_code_block(text):
        return block_type_code
    if is_markdown_quote_block(text):
        return block_type_quote
    if is_markdown_unordered_list_block(text):
        return block_type_unordered_list
    if is_markdown_ordered_list_block(text):
        return block_type_ordered_list
    return block_type_paragraph


# tag, value, children, props


def heading_block_to_html_node(block: str) -> ParentNode:
    match = re.match(r"^(#{1,6})\s+(.+)$", block)
    if match:
        count = len(match.group(1))
        text = block[count + 1 :]
        children = text_to_children(text)
        return ParentNode(f"h{count}", children)
    raise ValueError(f"Invalid heading block: {text}")


def code_block_to_html_node(block: str) -> ParentNode:
    # wrap in pre tag
    text = block.strip("```")
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_block_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote")
        new_lines.append(line.strip("> "))
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    # wrap in ol tag
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def unordered_list_to_html_node(block: str) -> ParentNode:
    # wrap in ul tag
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def paragraph_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    if children:
        return ParentNode("p", children)
    raise ValueError("No children in paragraph")


def text_to_children(text: str) -> [HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_block_to_html_node(block)
    if block_type == block_type_code:
        return code_block_to_html_node(block)
    if block_type == block_type_quote:
        return quote_block_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_html_node(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_html_node(block)
    raise ValueError("invalid block type")


def is_markdown_heading_block(text: str) -> bool:
    heading_pattern = re.compile(r"^#{1,6}\s+.+$")
    return bool(heading_pattern.match(text))


def is_markdown_code_block(text: str) -> bool:
    code_pattern = re.compile(r"^```[\s\S]*```$")
    return bool(code_pattern.match(text))


def is_markdown_quote_block(text: str) -> bool:
    quote_pattern = re.compile(r"^(>.*(\n|$))+$")
    return bool(quote_pattern.match(text))


def is_markdown_unordered_list_block(text: str) -> bool:
    unordered_list_pattern = re.compile(r"^([\*-].*(\n|$))+$")
    return bool(unordered_list_pattern.match(text))


def is_markdown_ordered_list_block(text: str) -> bool:
    ordered_list_pattern = re.compile(r"^((\d+\..*)(\n|$))+$")
    return bool(ordered_list_pattern.match(text))
