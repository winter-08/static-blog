import re

from htmlnode import HTMLNode
from textnode import text_to_textnodes, text_node_to_html_node

def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n")
    blocks = [item.strip() for item in blocks if item.strip()]
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

#tag, value, children, props

def heading_block_to_html_node(text: str) -> HTMLNode:
    match = re.match(r'^(#{1,6})\s+(.+)$', text)
    if match:
        count = len(match.group(1))
        tag = f"h{count}"
        value = match.group(2)
        node = HTMLNode(tag, value, None, None)
        return node
    else:
        raise ValueError(f"Invalid heading block: {text}")

def code_block_to_html_node(text: str) -> HTMLNode:
    #wrap in pre tag
    text_raw = text.strip('```')
    node = HTMLNode("pre", None, [HTMLNode("code", text_raw, None, None)], None)
    return node

def quote_block_to_html_node(text: str) -> HTMLNode:
    text_raw = text.strip('>')
    node = HTMLNode("blockquote", text_raw, None, None)
    return node

def ordered_list_to_html_node(text: str) -> HTMLNode:
    #wrap in ol tag
    text_raw = text.split('. ', 2)
    node = HTMLNode("ol", text_raw, None, None)
    return node

def unordered_list_to_html_node(text: str) -> HTMLNode:
    #wrap in ul tag
    text_raw = text.strip('-')
    text_raw = text.strip('*')
    node = HTMLNode("ul", text_raw, None, None)
    return node

def markdown_to_html_node(markdown: str) -> list[HTMLNode]:
    html_node = HTMLNode("div", None, [], None)
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            html_node.children.append(heading_block_to_html_node(block))
        if block_type == block_type_code:
            html_node.children.append(code_block_to_html_node(block))
        if block_type == block_type_quote:
            html_node.children.append(quote_block_to_html_node(block))
        if block_type == block_type_ordered_list:
            html_node.children.append(block_type_ordered_list(block))
        if block_type == block_type_unordered_list:
            html_node.children.append(unordered_list_to_html_node(block))
        else:
            nodes = text_to_textnodes(block.value)
            html_node.children.append(HTMLNode("p", "", lambda node: text_node_to_html_node(node), nodes))
    return html_node

    
def is_markdown_heading_block(text: str) -> bool:
    heading_pattern = re.compile(r'^#{1,6}\s+.+$')
    return bool(heading_pattern.match(text))

def is_markdown_code_block(text: str) -> bool:
    code_pattern = re.compile(r'^```[\s\S]*```$')
    return bool(code_pattern.match(text))

def is_markdown_quote_block(text: str) -> bool:
    quote_pattern = re.compile(r'^(>.*(\n|$))+$')
    return bool(quote_pattern.match(text))

def is_markdown_unordered_list_block(text: str) -> bool:
    unordered_list_pattern = re.compile(r'^([\*-].*(\n|$))+$')
    return bool(unordered_list_pattern.match(text))

def is_markdown_ordered_list_block(text: str) -> bool:
    ordered_list_pattern = re.compile(r'^((\d+\..*)(\n|$))+$')
    return bool(ordered_list_pattern.match(text))
