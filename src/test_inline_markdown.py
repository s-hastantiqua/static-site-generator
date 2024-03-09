import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_link,
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
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


class TestSplitNodesExtended(unittest.TestCase):

    def test_split_nodes_image_empty_string(self):
        original_nodes = [TextNode("", text_type_text)]
        expected_nodes = []
        result_nodes = split_nodes_image(original_nodes)
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_nodes_image_multiple_images(self):
        original_nodes = [TextNode("![alt1](http://example.com/image1.jpg) ![alt2](http://example.com/image2.jpg)", text_type_text)]
        expected_nodes = [
            TextNode("alt1", text_type_image, "http://example.com/image1.jpg"),
            TextNode(" ", text_type_text),
            TextNode("alt2", text_type_image, "http://example.com/image2.jpg")
        ]
        result_nodes = split_nodes_image(original_nodes)
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_nodes_image_mixed_content(self):
        original_nodes = [TextNode("Text ![alt](http://example.com/image.jpg) more text", text_type_text)]
        expected_nodes = [
            TextNode("Text ", text_type_text),
            TextNode("alt", text_type_image, "http://example.com/image.jpg"),
            TextNode(" more text", text_type_text)
        ]
        result_nodes = split_nodes_image(original_nodes)
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_nodes_link_empty_string(self):
        original_nodes = [TextNode("", text_type_text)]
        expected_nodes = []
        result_nodes = split_nodes_link(original_nodes)
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_nodes_link_multiple_links(self):
        original_nodes = [TextNode("[link1](http://example1.com) [link2](http://example2.com)", text_type_text)]
        expected_nodes = [
            TextNode("link1", text_type_link, "http://example1.com"),
            TextNode(" ", text_type_text),
            TextNode("link2", text_type_link, "http://example2.com")
        ]
        result_nodes = split_nodes_link(original_nodes)
        self.assertEqual(result_nodes, expected_nodes)

    def test_split_nodes_link_mixed_content(self):
        original_nodes = [TextNode("Text before [link](http://example.com) text after", text_type_text)]
        expected_nodes = [
            TextNode("Text before ", text_type_text),
            TextNode("link", text_type_link, "http://example.com"),
            TextNode(" text after", text_type_text)
        ]
        result_nodes = split_nodes_link(original_nodes)
        self.assertEqual(result_nodes, expected_nodes)


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "This is plain text."
        expected = [TextNode("This is plain text.", text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        expected = [TextNode("This is ", text_type_text), TextNode("bold", text_type_bold), TextNode(" text.", text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        expected = [TextNode("This is ", text_type_text), TextNode("italic", text_type_italic), TextNode(" text.", text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_text(self):
        text = "This is `code` text."
        expected = [TextNode("This is ", text_type_text), TextNode("code", text_type_code), TextNode(" text.", text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "This is ![alt text](http://example.com/image.jpg) in text."
        expected = [TextNode("This is ", text_type_text), TextNode("alt text", text_type_image, "http://example.com/image.jpg"), TextNode(" in text.", text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "This is [link text](http://example.com) in text."
        expected = [TextNode("This is ", text_type_text), TextNode("link text", text_type_link, "http://example.com"), TextNode(" in text.", text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_combined_markdown_elements(self):
        text = "**Bold**, *italic*, `code`, ![alt](http://image.com), [link](http://link.com)."
        expected = [
            TextNode("Bold", text_type_bold), TextNode(", ", text_type_text),
            TextNode("italic", text_type_italic), TextNode(", ", text_type_text),
            TextNode("code", text_type_code), TextNode(", ", text_type_text),
            TextNode("alt", text_type_image, "http://image.com"), TextNode(", ", text_type_text),
            TextNode("link", text_type_link, "http://link.com"), TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_nested_bold_italic(self):
        text = "This is **bold and *italic* text**."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold and ", text_type_bold),
            TextNode("italic", text_type_italic),
            TextNode(" text", text_type_bold),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link_inside_bold(self):
        text = "This is **bold with a [link](http://example.com)** text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold with a ", text_type_bold),
            TextNode("link", text_type_link, "http://example.com"),
            TextNode(" text.", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image_inside_italic(self):
        text = "This is *italic with an ![image](http://example.com/image.jpg)* text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("italic with an ", text_type_italic),
            TextNode("image", text_type_image, "http://example.com/image.jpg"),
            TextNode(" text.", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_complex_nesting(self):
        text = "Here is **bold, *italic, and ![an image](http://example.com/image.jpg)* text**."
        expected = [
            TextNode("Here is ", text_type_text),
            TextNode("bold, ", text_type_bold),
            TextNode("italic, and ", text_type_italic),
            TextNode("an image", text_type_image, "http://example.com/image.jpg"),
            TextNode(" text", text_type_bold),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == '__main__':
    unittest.main()
