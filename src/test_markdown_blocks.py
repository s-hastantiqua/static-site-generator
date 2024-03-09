import unittest

from markdown_blocks import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks,
    block_to_block_type
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

    def test_block_type_empty_code_block(self):
        # Code block must not be empty
        empty_code_block = "```\n```"
        self.assertEqual(block_to_block_type(empty_code_block), block_type_paragraph)


if __name__ == '__main__':
    unittest.main()
