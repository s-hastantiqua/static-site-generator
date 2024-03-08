import unittest

from htmlnode import LeafNode
from textnode import (
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    TextNode,
    text_node_to_html_node,
    split_nodes_delimiter
)


class TestTextNode(unittest.TestCase):
 
    def test_textnode_creation(self):
        node1 = TextNode("Sample text", "title")
        self.assertEqual(node1.text, "Sample text")
        self.assertEqual(node1.text_type, "title")
        self.assertIsNone(node1.url)

        node2 = TextNode("Another text", "body", "http://example.com")
        self.assertEqual(node2.text, "Another text")
        self.assertEqual(node2.text_type, "body")
        self.assertEqual(node2.url, "http://example.com")

    def test_equality(self):
        node1 = TextNode("Text 1", "title", "http://example.com")
        node2 = TextNode("Text 1", "title", "http://example.com")
        node3 = TextNode("Text 2", "title", "http://example.com")
        node4 = TextNode("Text 1", "body", "http://example.com")
        node5 = TextNode("Text 1", "title")

        self.assertEqual(node1, node2)

        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        self.assertNotEqual(node1, node5)

    def test_representation(self):
        node = TextNode("Sample text", "title", "http://example.com")
        expected_repr = "TextNode(Sample text, title, http://example.com)"
        self.assertEqual(repr(node), expected_repr)


class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text_node_to_html_text(self):
        text_node = TextNode("Just text", text_type_text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(None, "Just text"))

    def test_text_node_to_html_bold(self):
        text_node = TextNode("Bold text", text_type_bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("b", "Bold text"))

    def test_text_node_to_html_italic(self):
        text_node = TextNode("Italic text", text_type_italic)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("i", "Italic text"))

    def test_text_node_to_html_code(self):
        text_node = TextNode("Code text", text_type_code)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("code", "Code text"))

    def test_text_node_to_html_link(self):
        text_node = TextNode("Link text", text_type_link, url="http://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("a", "Link text", {"href": "http://example.com"}))

    def test_text_node_to_html_image(self):
        text_node = TextNode("Image alt", text_type_image, url="http://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode("img", "", {"src": "http://example.com/image.png", "alt": "Image alt"}))

    def test_invalid_text_type(self):
        text_node = TextNode("Invalid", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_valid_delimiter_bold_with_multiple_nodes(self):
        original_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("**bold text**", text_type_text),
            TextNode(" in a sentence with **another bold part**.", text_type_text)
        ]
        split_nodes = split_nodes_delimiter(original_nodes, "**", text_type_bold)
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("bold text", text_type_bold),
            TextNode(" in a sentence with ", text_type_text),
            TextNode("another bold part", text_type_bold),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_valid_delimiter_italic_with_multiple_nodes(self):
        original_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("*italic text* in a sentence with *another italic part*.", text_type_text)
        ]
        split_nodes = split_nodes_delimiter(original_nodes, "*", text_type_italic)
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("italic text", text_type_italic),
            TextNode(" in a sentence with ", text_type_text),
            TextNode("another italic part", text_type_italic),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_valid_delimiter_code_with_multiple_nodes(self):
        original_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("`code block`", text_type_text),
            TextNode(" in a sentence with `another code block`.", text_type_text)
        ]
        split_nodes = split_nodes_delimiter(original_nodes, "`", text_type_code)
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" in a sentence with ", text_type_text),
            TextNode("another code block", text_type_code),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(split_nodes, expected_nodes)

    def test_split_nodes_invalid_syntax(self):
        original_nodes = [TextNode("Unbalanced `code", text_type_text)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(original_nodes, "`", text_type_code)

    def test_split_nodes_empty_result(self):
        original_nodes = [TextNode("``", text_type_text)]
        split_nodes = split_nodes_delimiter(original_nodes, "`", text_type_code)
        self.assertEqual(len(split_nodes), 0)


if __name__ == "__main__":
    unittest.main()
