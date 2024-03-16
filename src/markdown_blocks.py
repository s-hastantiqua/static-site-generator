import re

from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode


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
        filtered_blocks.append(block.strip())
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
    return text.startswith("```") and text.endswith("```")


def is_quote_block(text) -> bool:
    pattern = r"^>.*"
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


def text_to_children(text) -> list:
    text_nodes = text_to_textnodes(text.strip())
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block) -> ParentNode:
    level_markers, text = block.split(" ", 1)
    level = len(level_markers)
    
    if not 1 <= level <= 6:
        raise ValueError(f"Invalid heading level: {level_markers}. Heading level must be between 1 and 6.")
    
    if not text:
        raise ValueError("Heading text cannot be empty.")
    
    tag = f"h{level}"
    children = text_to_children(text)
    return ParentNode(tag, children)


def code_to_html_node(block) -> ParentNode:
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_html_node(block) -> ParentNode:
    text = '\n'.join(line.lstrip("> ").strip() for line in block.split("\n"))
    return markdown_to_html_node(text, "blockquote")


def unordered_list_to_html_node(block) -> ParentNode:
    list_items = block.split("\n")
    html_items = []
    for item in list_items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block) -> ParentNode:
    list_items = block.split("\n")
    html_items = []
    for item in list_items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def block_to_html_node(block, block_type) -> ParentNode:
    type_to_func = {
        block_type_paragraph: paragraph_to_html_node,
        block_type_heading: heading_to_html_node,
        block_type_code: code_to_html_node,
        block_type_quote: quote_to_html_node,
        block_type_unordered_list: unordered_list_to_html_node,
        block_type_ordered_list: ordered_list_to_html_node,
    }
    
    if block_type in type_to_func:
        return type_to_func[block_type](block)
    raise ValueError(f"Invalid block type: {block_type}")


def markdown_to_html_node(markdown, tag) -> ParentNode:
    child_elements = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        child_elements.append(html_node)
    return ParentNode(tag, child_elements)
