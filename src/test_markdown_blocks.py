import unittest

from bs4 import BeautifulSoup


from markdown_blocks import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node
)


class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_paragraph(self):
        markdown = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_paragraphs(self):
        markdown = "This is the first paragraph.\n\nThis is the second paragraph."
        expected = ["This is the first paragraph.", "This is the second paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_mixed_content(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line                

* This is a list
* with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_whitespace_around_blocks(self):
        markdown = """

        This paragraph has whitespace around it.    
        
        """
        expected = ["This paragraph has whitespace around it."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_new_lines_within_paragraph(self):
        markdown = "This is a paragraph\nwith a new line\nbut considered as one block."
        expected = ["This is a paragraph\nwith a new line\nbut considered as one block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)


class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), block_type_heading)
        self.assertEqual(block_to_block_type("## Heading 2 with **bold** text"), block_type_heading)

    def test_block_to_block_type_code(self):
        code_block = "```\ndef example():\n    return 'example'\n```"
        self.assertEqual(block_to_block_type(code_block), block_type_code)

    def test_block_to_block_type_quote(self):
        quote_block = "> This is a quote\n> This is the second line of the quote"
        self.assertEqual(block_to_block_type(quote_block), block_type_quote)

    def test_block_to_block_type_unordered_list(self):
        unordered_list_block = "* Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(unordered_list_block), block_type_unordered_list)

        unordered_list_block_dash = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(unordered_list_block_dash), block_type_unordered_list)

    def test_block_to_block_type_ordered_list(self):
        ordered_list_block = "1. First item\n2. Second item"
        self.assertEqual(block_to_block_type(ordered_list_block), block_type_ordered_list)

    def test_block_to_block_type_paragraph(self):
        paragraph = "This is a paragraph with some text."
        self.assertEqual(block_to_block_type(paragraph), block_type_paragraph)

        mixed_content = "This is a paragraph with **bold** and *italic* text."
        self.assertEqual(block_to_block_type(mixed_content), block_type_paragraph)
    
    def test_block_type_misordered_ordered_list(self):
        # Numbers missing or in wrong order
        misordered_list = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(misordered_list), block_type_paragraph)

        wrong_order_list = "2. Second item\n1. First item"
        self.assertEqual(block_to_block_type(wrong_order_list), block_type_paragraph)

    def test_block_type_incomplete_quote(self):
        # Not all lines start with ">"
        incomplete_quote = "> This is a quote\nThis line is not part of the quote"
        self.assertEqual(block_to_block_type(incomplete_quote), block_type_paragraph)

    def test_block_type_mixed_unordered_list_symbols(self):
        # Mixed symbols "*" and "-"
        mixed_list = "* First item\n- Second item"
        self.assertEqual(block_to_block_type(mixed_list), block_type_paragraph)

    def test_block_type_ordered_list_with_missing_dot(self):
        # Missing "." symbol after number
        missing_dot_list = "1 First item\n2 Second item"
        self.assertEqual(block_to_block_type(missing_dot_list), block_type_paragraph)


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_complex_markdown_example(self):
        document = """
# Complex Markdown Example

This paragraph includes **bold**, *italic*, and `inline code`.

## Lists

- Unordered list item 1
- Unordered list item 2
- Unordered list item 3 with a [link](http://example.com)

1. Ordered list item 1
2. Ordered list item 2
3. Ordered list item 3

![Alt text for an image](http://example.com/image.jpg)

> This is a quote block.
>
> - List inside a quote
> - Another list item
>
> More quoted text.

## Code Block

```
def example_function():
    # This is a comment
    print("Hello, World!")
```

This is a paragraph following a code block. And here's a link in a paragraph: [Example Link](http://example.com).
"""
        expected = """
<div><h1>Complex Markdown Example</h1><p>This paragraph includes <b>bold</b>, <i>italic</i>, and <code>inline code</code>.</p><h2>Lists</h2><ul><li>Unordered list item 1</li><li>Unordered list item 2</li><li>Unordered list item 3 with a <a href="http://example.com">link</a></li></ul><ol><li>Ordered list item 1</li><li>Ordered list item 2</li><li>Ordered list item 3</li></ol><p><img src="http://example.com/image.jpg" alt="Alt text for an image" /></p><blockquote><p>This is a quote block.</p><ul><li>List inside a quote</li><li>Another list item</li></ul><p>More quoted text.</p></blockquote><h2>Code Block</h2><pre><code>def example_function():
    # This is a comment
    print("Hello, World!")</code></pre><p>This is a paragraph following a code block. And here's a link in a paragraph: <a href="http://example.com">Example Link</a>.</p></div>
    """
        expected_soup = BeautifulSoup(expected, 'html.parser').prettify()
        actual_soup = BeautifulSoup(markdown_to_html_node(document, "div").to_html(), 'html.parser').prettify()
        self.assertEqual(str(expected_soup), str(actual_soup))

if __name__ == '__main__':
    unittest.main()
