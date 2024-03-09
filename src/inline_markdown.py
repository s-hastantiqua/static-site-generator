import re

from textnode import TextNode, text_type_image, text_type_link


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        original_text_type = old_node.text_type
        if original_text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown syntax")
        sections = original_text.split(delimiter)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], original_text_type))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes) -> list:
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        original_text_type = old_node.text_type
        if original_text == "":
            continue
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for alt_text, src in images:
            sections = original_text.split(f"![{alt_text}]({src})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], original_text_type))
            new_nodes.append(TextNode(alt_text, text_type_image, src))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, original_text_type))
    return new_nodes


def split_nodes_link(old_nodes) -> list:
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        original_text_type = old_node.text_type
        if original_text == "":
            continue
        links = extract_markdown_link(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link_text, href in links:
            sections = original_text.split(f"[{link_text}]({href})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], original_text_type))
            new_nodes.append(TextNode(link_text, text_type_link, href))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, original_text_type))
    return new_nodes


def extract_markdown_images(text) -> list:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_link(text) -> list:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
