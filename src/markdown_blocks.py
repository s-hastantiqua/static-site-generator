import re


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown) -> list:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block) -> str:
    if is_heading_block(block):
        return block_type_heading
    if is_code_block(block):
        return block_type_code
    if is_quote_block(block):
        return block_type_quote
    if is_unordered_list_block(block):
        return block_type_unordered_list
    if is_ordered_list_block(block):
        return block_type_ordered_list
    return block_type_paragraph


def is_heading_block(text) -> bool:
    pattern = r"^(#{1,6})\s+(.+)"
    match = re.match(pattern, text)
    return match is not None


def is_code_block(text) -> bool:
    return text.startswith("```") and text.endswith("```") and text.strip("```").strip() != ""


def is_quote_block(text) -> bool:
    pattern = r"^> .+"
    return all(re.match(pattern, line.strip()) for line in text.split("\n"))


def is_unordered_list_block(text) -> bool:
    lines = text.split("\n")
    pattern_star = r"^\* .+"
    pattern_dash = r"^- .+"
    
    all_star = all(re.match(pattern_star, line.strip()) for line in lines)
    all_dash = all(re.match(pattern_dash, line.strip()) for line in lines)
    
    return all_star or all_dash


def is_ordered_list_block(text) -> bool:
    lines = text.split("\n")
    for i, line in enumerate(lines, start=1):
        pattern = r"^" + str(i) + r"\. .+"
        if not re.match(pattern, line.strip()):
            return False
    return True
