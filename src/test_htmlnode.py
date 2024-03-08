import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_htmlnode_creation(self):
        node = HTMLNode("div", "Hello, world!", children=[HTMLNode("p", "This is a paragraph.")], props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].value, "This is a paragraph.")
        self.assertEqual(node.props["class"], "container")

    def test_to_html(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "container"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "container"})
        expected_props_html = ' class="container"'
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_representation(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "container"})
        expected_repr = "HTMLNode(div, Hello, world!, children: None, {'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)


if __name__ == '__main__':
    unittest.main()
