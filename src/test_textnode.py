import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
 
    def test_textnode_creation(self):
        # Test creating a TextNode instance with no URL
        node1 = TextNode("Sample text", "title")
        self.assertEqual(node1.text, "Sample text")
        self.assertEqual(node1.text_type, "title")
        self.assertIsNone(node1.url)

        # Test creating a TextNode instance with a URL
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

        # Test equality between two TextNode instances with the same attributes
        self.assertEqual(node1, node2)

        # Test inequality between two TextNode instances with different attributes
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        self.assertNotEqual(node1, node5)

    def test_representation(self):
        node = TextNode("Sample text", "title", "http://example.com")
        expected_repr = "TextNode(Sample text, title, http://example.com)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
