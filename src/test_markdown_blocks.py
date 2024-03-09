import unittest

from markdown_blocks import markdown_to_blocks


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


if __name__ == '__main__':
    unittest.main()
