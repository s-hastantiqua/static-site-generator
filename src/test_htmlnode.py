import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    def test_initialization(self):
        node = HTMLNode(tag='div', value='Hello, World!', children=None, props={'class': 'my-class'})
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'Hello, World!')
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'class': 'my-class'})

    def test_props_to_html(self):
        node = HTMLNode(props={'class': 'test', 'id': 'unique'})
        self.assertEqual(node.props_to_html(), ' class="test" id="unique"')

    def test_repr(self):
        node = HTMLNode('span', 'Example', None, {'style': 'color: red;'})
        expected_repr = "HTMLNode(span, Example, children: None, {'style': 'color: red;'})"
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):

    def test_initialization_and_repr(self):
        leaf = LeafNode(tag='p', value='This is a paragraph.', props={'class': 'text'})
        expected_repr = "LeafNode(p, This is a paragraph., {'class': 'text'})"
        self.assertEqual(repr(leaf), expected_repr)

    def test_to_html_with_tag_and_props(self):
        leaf = LeafNode('p', 'This is a paragraph.', {'class': 'text'})
        self.assertEqual(leaf.to_html(), '<p class="text">This is a paragraph.</p>')

    def test_to_html_without_props(self):
        leaf = LeafNode('span', 'A span element')
        self.assertEqual(leaf.to_html(), '<span>A span element</span>')

    def test_to_html_with_none_tag(self):
        leaf = LeafNode(tag=None, value='Just some text.')
        self.assertEqual(leaf.to_html(), 'Just some text.')

    def test_value_error_on_empty_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag='p', value=None, props={'class': 'text'})


if __name__ == '__main__':
    unittest.main()
