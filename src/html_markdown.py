def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n")
    blocks = [item.strip() for item in blocks if item.strip()]
    return blocks 
