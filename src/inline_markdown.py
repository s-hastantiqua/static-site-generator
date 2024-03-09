import re

from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        if text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown syntax")
        sections = text.split(delimiter)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], old_node.text_type))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes


def extract_markdown_images(text) -> list:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_link(text) -> list:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
