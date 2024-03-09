import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_link
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code
)


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


class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images_basic(self):
        text = "![alt text](http://example.com/image.jpg)"
        expected = [("alt text", "http://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_with_multiple_images(self):
        text = "![alt1](http://example.com/image1.jpg) and ![alt2](http://example.com/image2.png)"
        expected = [("alt1", "http://example.com/image1.jpg"), ("alt2", "http://example.com/image2.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_with_text_between(self):
        text = "Text before ![alt](http://example.com/image.jpg) text after"
        expected = [("alt", "http://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_image(self):
        text = "No images here"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_link_basic(self):
        text = "[link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_link(text), expected)

    def test_extract_markdown_link_with_multiple_links(self):
        text = "[link1](http://example1.com) and [link2](http://example2.com)"
        expected = [("link1", "http://example1.com"), ("link2", "http://example2.com")]
        self.assertEqual(extract_markdown_link(text), expected)

    def test_extract_markdown_link_with_text_between(self):
        text = "Text before [link](http://example.com) text after"
        expected = [("link", "http://example.com")]
        self.assertEqual(extract_markdown_link(text), expected)

    def test_extract_markdown_link_no_link(self):
        text = "No links here"
        expected = []
        self.assertEqual(extract_markdown_link(text), expected)

    def test_extract_markdown_mixed_content(self):
        text = "An image ![alt](http://example.com/image.jpg) and a link [link](http://example.com) in the same text."
        expected_image = [("alt", "http://example.com/image.jpg")]
        expected_link = [("link", "http://example.com")]
        self.assertEqual(extract_markdown_images(text), expected_image)
        self.assertEqual(extract_markdown_link(text), expected_link)


if __name__ == '__main__':
    unittest.main()
